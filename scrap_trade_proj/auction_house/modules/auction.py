
import sys
from django.conf import settings
from django.shortcuts import get_object_or_404

from auction_house.models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
    AhAnswerLine,
    Catalog,
    AhMatClass,
)

from state_wf.models import (
    StepState,
)
from notification.modules import ntf_manager
from project_main.models import Project

from django.urls import reverse
from notification.modules import ntf_manager
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from customers.models import (
    Customer,
)
from django.utils.dateparse import parse_datetime
import django.utils.timezone as django_timezone

from datetime import (
    date,
    datetime,
    timedelta,
)



class AuctionSection:

    def __init__(self,
                 par_title='title',
                 par_list=list(),
                 ):
        self.title = par_title
        self.lines = par_list

    def __repr__(self):
        return "AuctionSection('{}', {})"\
            .format(self.title, self.lines)

    def __str__(self):
        return self.title


class AuctionLine:

    def __init__(self,
                 par_title='title',
                 par_count=0,
                 par_state_key='Not set',
                 par_url_key=None,
                 ):
        self.title = par_title
        self.member_count = par_count
        self.state_key = par_state_key
        self.url_key = par_url_key

    def __repr__(self):
        return "AuctionLine('{}', {}, '{}')"\
            .format(self.title, self.member_count, self.state_key)

    def __str__(self):
        return self.title



def resurect_auction(par_offer):
    print('resurect offer: {}'.format(par_offer))
    state_obj = StepState.objects.get(state_key='offer_in_auction')
    offer_add_state(par_offer, state_obj, None)
    answer_canceled = StepState.objects.get(state_key='answer_canceled')
    state_obj = StepState.objects.get(state_key='answer_in_auction')
    for set_a in par_offer.answers.all():
        if set_a.actual_state != answer_canceled:
            print('resurect answer: {}'.format(set_a))
            answer_add_state(set_a, state_obj, None)
        set_a.is_bound = False
        set_a.save()
    return

def offer_no_answers(request, par_offer):
    # cancel offer - no anwers
    print('cancel - no answers - {}'.format(par_offer))
    # kill offer
    state_obj = StepState.objects.get(state_key='offer_canceled')
    offer_add_state(par_offer, state_obj, None)
    ntf_send_from_auction(
        request=request,
        place='modules.auction - set_auction() - no answers',
        offer_description=par_offer.description,
        customer=par_offer.owner,
        template='offer_no_answers',
        admins=False,
        business=True,
    )

def kill_new_answers(par_offer):
    new_answers = filter_by_state(par_offer.answers, 'answer_new')
    for kill_answer in new_answers:
        print('kill answer = {}'.format(kill_answer))
        answer_add_state(kill_answer, state_obj, None)
    return

def start_auction(request, par_offer):
    print('Start auction: {} at {}'.format(par_offer, par_offer.auction_start))
    if settings.AUTO_ANSWERS:
        my_answers = except_state(par_offer.answers, 'answer_canceled')
    else:
        kill_new_answers(par_offer)
        my_answers = filter_by_state(par_offer.answers, 'answer_confirmed')
    if my_answers.count() > 0 :
        state_in_auction = StepState.objects.get(state_key='offer_in_auction')
        offer_add_state(par_offer, state_in_auction, None)
        state_a_auction = StepState.objects.get(state_key='answer_in_auction')
        ntf_send_from_auction(
            request=request,
            place='modules.auction - start_auction() - offer',
            offer_description=par_offer.description,
            customer=par_offer.owner,
            template='auction_started',
            admins=False,
            business=True,
            set_url=par_offer.auction_url,
        )
        mess_list = list()
        context = ntf_manager.NtfContext()
        context['place'] = 'modules.auction - start_auction() - answers'
        context['offer_description'] = par_offer.description
        for answer in my_answers:
            answer_add_state(answer, state_a_auction, None)
            message = ntf_create_from_auction(
                template='auction_started',
                context=context.clone_context(),
                cust_url=answer.auction_url,
                customer=answer.owner,
                admins=False,
                business=True,
            )
            mess_list.append(message)
        ntf_manager.send_via_ntf(request, mess_list, context)
    else:
        offer_no_answers(request, par_offer)
    return

def accept_answer(request, par_answer, par_place, par_user):
    state_send = _get_state('offer_accepted')
    offer_add_state(par_answer.ah_offer, state_send, par_user)
    if state_send.send_ntf:
        print('send to offer')
        ntf_send_from_view(
        request=request,
        state=state_send,
        place=par_place,
        item=par_answer.ah_offer,
    )


def set_auction(request, par_offer, par_answer_state):
    print('from second: {} must be set / {}'.format(par_offer, par_offer.auction_date))
    state_obj = StepState.objects.get(state_key='answer_canceled')
    # kill not confirmed Answers
    if settings.AUTO_ANSWERS:
        my_answers = except_state(par_offer.answers, 'answer_canceled')
    else:
        kill_new_answers(par_offer)
        my_answers = filter_by_state(par_offer.answers, par_answer_state)

    if my_answers.count() > 0 :
        # vyhodnoceni
        print('vyhodnoceni {}'.format(par_offer))
        # set offer in auction
        if par_offer.actual_state.state_key != 'offer_in_auction':
            state_in_auction = StepState.objects.get(state_key='offer_in_auction')
            offer_add_state(par_offer, state_in_auction, None)
        # find and mark succesfull
        lucky_one = my_answers.all().order_by('-total_price').first()
        print('set to {}'.format(lucky_one))
        state_obj = StepState.objects.get(state_key='answer_successful')
        answer_add_state(lucky_one, state_obj, None)
        lucky_one.is_bound = True
        lucky_one.save()
        # send report
        if state_obj.send_ntf:
            ntf_send_from_view(
                request=request,
                state=state_obj,
                place='modules.auction - set_auction()',
                item=lucky_one,
            )
        # auto confirm
        if settings.DIRECT_ANSWER_ACCEPT:
            print('auto-accept')
            set_state = _get_state('answer_accepted')
            answer_add_state(lucky_one, set_state, None)
            accept_answer(request, lucky_one, 'Auto-accept', None)

        # unbound others
        state_obj = StepState.objects.get(state_key='answer_closed')
        for unlucky_one in filter_by_state(par_offer.answers, par_answer_state):
            print('close {}'.format(unlucky_one))
            answer_add_state(unlucky_one, state_obj, None)
            ntf_send_from_auction(
                request=request,
                place='modules.auction - set_auction() - closed',
                offer_description=par_offer.description,
                customer=unlucky_one.owner,
                template='auction_ended',
                admins=False,
                business=True,
            )

    else:
        offer_no_answers(request, par_offer)
    return

def make_auctions(request, par_ref_dt):
    dt_ref = parse_datetime(par_ref_dt)
    if not django_timezone.is_aware(dt_ref):
        dt_ref = django_timezone.make_aware(dt_ref)
    print('make auction at {}'.format(dt_ref))
    my_offers = filter_by_state(AhOffer.objects.all(), 'offer_confirmed')
    for offer in my_offers:
        auction_dt = datetime.combine(offer.auction_date, datetime.min.time())
        if not django_timezone.is_aware(auction_dt):
            auction_dt = django_timezone.make_aware(auction_dt)
        if auction_dt <= dt_ref:
            set_auction(request, offer, 'answer_confirmed')
        else:
            print('{} is waiting / {}'.format(offer, offer.auction_date))
    return

def online_manager(request, par_ref_dt):
    dt_ref = parse_datetime(par_ref_dt)
    print('online manager at {}'.format(dt_ref))
    dt_ref_add_5 = dt_ref + timedelta(minutes=5)
    #----- evaluate online auctions
    eval_offers = filter_by_state(AhOffer.objects.all(), 'offer_in_auction')
    print('eval_offers = {}'.format(eval_offers))
    for offer in eval_offers:
        if offer.auction_end <= dt_ref:
            set_auction(request, offer, 'answer_in_auction')
    #----- start online auctions
    start_offers = filter_by_state(AhOffer.objects.all(), 'offer_confirmed')
    print('start_offers = {}'.format(start_offers))
    for offer in start_offers:
        if offer.auction_start <= dt_ref_add_5:
            start_auction(request, offer)
    return

#-------------------------------- house views
def offer_to(par_customer):
    return Customer.objects.exclude(id = par_customer.pk)

def offer_add_state(offer_obj, state_obj, user):
    offer_obj.my_steps.create(
        state = state_obj,
        offer_link = offer_obj,
        answer_link = None,
        changed_by = user,
    )
    offer_obj.save()


def customer_offer_create(customer, user, data):
    new = AhOffer(
        description = data['description'],
        delivery_date = data['delivery_date'],
        auction_date = data['auction_date'],
        owner = customer,
        creator = user,
    )
    new.save()
    for cc in offer_to(customer):
        new.offered_to.add(cc)
    new.save()

    # fisrt step
    new_state = StepState.objects.get(state_key='offer_new')
    offer_add_state(new, new_state, user)

    return new.pk


def filter_by_state(p_data, p_state_key):
    state = StepState.objects.get(state_key = p_state_key)
    id_set = [x.id for x in p_data.all() if x.is_equal_state(state)]
    return p_data.filter(id__in = id_set)

def except_state(p_data, p_state_key):
    state = StepState.objects.get(state_key = p_state_key)
    print('state = {}'.format(state))
    id_set = [x.id for x in p_data.all() if not x.is_equal_state(state)]
    print('id_set = {}'.format(id_set))
    return p_data.filter(id__in = id_set)


def answer_add_state(answer_obj, state_obj, user):
    answer_obj.my_steps.create(
        state = state_obj,
        offer_link = None,
        answer_link = answer_obj,
        changed_by = user,
    )
    answer_obj.save()

def customer_answer_create(request, customer, offer, user, data):

    new = AhAnswer(
        description = data['description'],
        owner = customer,
        ah_offer = offer,
        creator = user,
        changed_by = user,
    )
    new.save()
    new.auction_url = request.build_absolute_uri(reverse('realtime-auction', kwargs={'pk': new.id, 'pk2': offer.id}))
    new.save()
    new_state = StepState.objects.get(state_key='answer_new')
    answer_add_state(new, new_state, user)
    for line in offer.lines.all():
        n_a_l = AhAnswerLine(
            answer = new,
            offer_line = line,
        )
        n_a_l.save()

def get_waiting_offers(par_customer):
    ret_offers = filter_by_state(par_customer.recieve_offers.all(), 'offer_confirmed')
    for answer in par_customer.owned_answers.all():
        ret_offers = ret_offers.exclude(id = answer.ah_offer.pk)
    return ret_offers.order_by("-pk")

def get_auction_list_control_obj(customer, data_offer, data_answers):
    ret_val = list()
    offer_list = list()
    for state in StepState.get_group_members(1):
        obj_line = AuctionLine(
            state.get_state_name_plural(),
            filter_by_state(data_offer, state.state_key).count(),
            state.state_key,
            'ah-customer-state-offers',
        )
        offer_list.append(obj_line)
    obj_offers = AuctionSection(
        _('Offers:'),
        offer_list,
    )
    ret_val.append(obj_offers)
    answer_list = list()
    if not settings.AUTO_ANSWERS:
        fist = AuctionLine(
            _('Wating offers'),
            get_waiting_offers(customer).count(),
            'Not set',
            'ah-customer-waiting-offers'
        )
        answer_list.append(fist)
    for state in StepState.get_group_members(2):
        obj_line = AuctionLine(
            state.get_state_name_plural(),
            filter_by_state(data_answers, state.state_key).count(),
            state.state_key,
            'ah-customer-state-answers',
        )
        answer_list.append(obj_line)
    obj_answers = AuctionSection(
        _('Answers:'),
        answer_list,
    )
    ret_val.append(obj_answers)
    return ret_val




def answer_update_ppu(answer_line):
    answer_line.total_price = answer_line.ppu * answer_line.offer_line.amount
    answer_line.save()
    answer_line.answer.refresh_total_price()
    return


def generate_answers(request, par_offer):
    for customer in par_offer.offered_to.all():
        #---- create answers
        new = AhAnswer(
            description = customer.customer_name,
            owner = customer,
            ah_offer = par_offer,
            creator = None,
            changed_by = None,
        )
        new.save()
        new.auction_url = request.build_absolute_uri(reverse('realtime-auction', kwargs={'pk': new.id, 'pk2': par_offer.id}))
        new.save()
        new_state = StepState.objects.get(state_key='answer_new')
        answer_add_state(new, new_state, None)
        for line in par_offer.lines.all():
            n_a_l = AhAnswerLine(
                #ppu = line.minimal_ppu,
                #total_price = line.amount * line.minimal_ppu,
                ppu = 0.0,
                total_price = 0.0,
                answer = new,
                offer_line = line,
            )
            n_a_l.save()
        new.refresh_total_price()
        new.save()

def _get_state(state_key):
    assert isinstance(state_key, str), "state_key must be a string"
    return get_object_or_404(StepState, state_key=state_key)


#--------------- notification ntf_support

def send_ntf_from_state(request, state, context):
    f_context = context.clone_context()
    #--- settings
    ret_val = True
    if 'item' in context:
        item = context['item']
    else:
        item = None
    #--- set context
    context['app_name'] = Project.objects.all().first().project_name
    #--- state depending
    #--- offer_confirmed
    if state.state_key == 'offer_confirmed':
        if type(item).__name__ != 'AhOffer':
            return False
        mess_list = list()
        if settings.AUTO_ANSWERS:
            print('item = {}'.format(item))
            for answer in item.answers.all():
                cust_url = request.build_absolute_uri(reverse('ah-answer-detail', args=[answer.pk]))
                message = ntf_create_from_auction(
                    template=state.ntf_template,
                    context=context.clone_context(),
                    cust_url=cust_url,
                    customer=answer.owner,
                    admins=False,
                    business=True,
                )
                mess_list.append(message)
        else:
            for customer in item.offered_to.all():
                cust_url = request.build_absolute_uri(reverse('ah-customer-answers-create', args=[customer.pk, item.pk]))
                message = ntf_create_from_auction(
                    template=state.ntf_template,
                    context=context.clone_context(),
                    cust_url=cust_url,
                    customer=customer,
                    admins=False,
                    business=True,
                )
                mess_list.append(message)
        ret_val = ntf_manager.send_via_ntf(request, mess_list, f_context)
    #---- answer_successful
    if state.state_key == 'answer_successful':
        if type(item).__name__ != 'AhAnswer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-answer-detail', args=[item.pk]))
        message = ntf_create_from_auction(
            template=state.ntf_template,
            context=context.clone_context(),
            cust_url=cust_url,
            customer=customer,
            admins=False,
            business=True,
        )
        ret_val = ntf_manager.send_via_ntf(request, message, f_context)
    #---- offer_accepted
    if state.state_key == 'offer_accepted':
        if type(item).__name__ != 'AhOffer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-offer-detail', args=[item.pk]))
        message = ntf_create_from_auction(
            template=state.ntf_template,
            context=context.clone_context(),
            cust_url=cust_url,
            customer=customer,
            admins=False,
            business=True,
        )
        ret_val = ntf_manager.send_via_ntf(request, message, f_context)
    #---- offer_ready_to_close
    if state.state_key == 'offer_ready_to_close':
        if type(item).__name__ != 'AhOffer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-offer-detail', args=[item.pk]))
        message = ntf_create_from_auction(
            template=state.ntf_template,
            context=context.clone_context(),
            cust_url=cust_url,
            customer=customer,
            admins=False,
            business=True,
        )
        ret_val = ntf_manager.send_via_ntf(request, message, f_context)
    return ret_val

def ntf_send_from_view(request, state, place='No where', item=None):
    try:
        context = ntf_manager.NtfContext()
        context['place'] = place
        context['item'] = item
        send_ntf_from_state(request, state, context)
    except:
        print('ntf_send_from_view error')
        print("Unexpected error:", sys.exc_info()[0])
    return

def ntf_send_from_auction(
    request,
    place='No where',
    offer_description="app",
    customer=None,
    template='fallback',
    admins=False,
    business=False,
    set_url="",
    ):
    try:
        context = ntf_manager.NtfContext()
        context['app_name'] = Project.objects.all().first().project_name
        context['place'] = place
        context['offer_description'] = offer_description
        if set_url != "":
            context['access_url'] = set_url
        ntf_manager.send_by_template(request, context, customer, template, admins, business)
    except:
        print('ntf_send_from_auction error')
        print("Unexpected error:", sys.exc_info()[0])

def ntf_create_from_auction(
    template='fallback',
    context=None,
    cust_url='Not set',
    customer=None,
    admins=False,
    business=False,
    ):
    try:
        message = ntf_manager.NtfMessage()
        message.template = template
        message.context = context
        message.context['access_url'] = cust_url
        message = customer.add_emails(message, False, True)
    except:
        print('ntf_create_from_auction error')
        print("Unexpected error:", sys.exc_info()[0])
    return
    return message


#-------- scrap special -------------
def set_cat_non_actual():
    for material in AhMatClass.objects.all():
        material.non_actual = True
        material.save()
    for c_e in Catalog.objects.all():
        c_e.non_actual = True
        c_e.save()
    return


def manage_materials(
    data_line,
):
    # ------------- Materials
    if AhMatClass.objects.filter(class_name=data_line.code).count() < 1:
        mat_line = AhMatClass(
            class_name=data_line.code,
            measurement_unit='T',
            base_description=data_line.description,
            is_dangerous=data_line.is_dangerous,
            non_actual=False,
            c_entry=data_line,
        )
        mat_line.save()
        mat_line.translations.create(
             model = mat_line,
             language = "cs",
             display_name = data_line.code,
             mat_class_description = data_line.description
        )
    else:
        mat_line = AhMatClass.objects.filter(class_name=data_line.code).first()
        mat_line.class_name = data_line.code
        mat_line.measurement_unit = 'T'
        mat_line.base_description=data_line.description
        mat_line.is_dangerous=data_line.is_dangerous
        mat_line.non_actual=False
        mat_line.c_entry=data_line
        mat_line.save()
        for trans in mat_line.translations.filter(language='cs'):
            trans.display_name = data_line.code
            trans.mat_class_description = data_line.description
            trans.save()
    return


def scrap_set_catalog(katalog):
    # ------- make old values not actual
    set_cat_non_actual()
    #-------- refresh from new values
    my_created = 0
    my_updated = 0
    for line in katalog:
        test = Catalog.objects.filter(code=line['code'])
        if test.count() < 1:
            data_line = Catalog(
                code=line['code'],
                description=line['description'],
                str_type=line['kind'],
            )
            data_line.save()
            my_created += 1
        else:
            data_line = test.first()
            data_line.code = line['code']
            data_line.description=line['description']
            data_line.str_type=line['kind']
            my_updated += 1
        if 'G' in data_line.str_type:
            data_line.is_group = True
        if 'N' in data_line.str_type:
            data_line.is_dangerous = True
        data_line.non_actual = False
        data_line.save()
        if data_line.is_group == False:
            manage_materials(data_line)

    message = 'Created {} lines. Updated {} lines. [{}]'\
        .format(my_created, my_updated, my_created+my_updated)
    return message
