
from django.shortcuts import get_object_or_404

from auction_house.models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
    AhAnswerLine
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
    state_obj = StepState.objects.get(state_key='offer_confirmed')
    offer_add_state(par_offer, state_obj, None)
    answer_canceled = StepState.objects.get(state_key='answer_canceled')
    state_obj = StepState.objects.get(state_key='answer_confirmed')
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

def set_auction(request, par_offer, par_answer_state):
    print('from second: {} must be set / {}'.format(par_offer, par_offer.auction_date))
    state_obj = StepState.objects.get(state_key='answer_canceled')
    # kill not confirmed Answers
    kill_new_answers(par_offer)
    my_answers = filter_by_state(par_offer.answers, par_answer_state)
    if my_answers.count() > 0 :
        # vyhodnoceni
        print('vyhodnoceni {}'.format(par_offer))
        # set offer in auction
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
    new_state = StepState.objects.filter(state_key='offer_new').first()
    offer_add_state(new, new_state, user)

def filter_by_state(p_data, p_state_key):
    state = StepState.objects.get(state_key = p_state_key)
    id_set = [x.id for x in p_data.all() if x.is_equal_state(state)]
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


def is_best_line(line):
    ret_val = False
    offer_line = line.offer_line
    best = offer_line.answer_lines.all().order_by('-total_price').first()
    ret_val = (best == line)
    return ret_val




def arrival_type_of_realtime_auction(offer):
    
    in_auction_state = StepState.objects.get(state_key = 'offer_in_auction')
    now = django_timezone.now()
    
    if now < offer.auction_start:
        arrival_type = 'too_soon'
    elif now > offer.auction_end:
        arrival_type = 'too_late'
    else:
        if offer.actual_state == in_auction_state:
            arrival_type = 'ok'
        else:
            arrival_type = 'wrong_state'
            # @todo; Something more meaningful should be reported
    
    return arrival_type



def get_classed_best_bids(price_sorted_bid_list,
                          owned_answer_id=None):
    best_bid_list = []
    
    for index, bid in enumerate(price_sorted_bid_list):
        classes = ['bid__item']
        if index == 0:
            classes.append('bid__item--best')
        if owned_answer_id == bid.id:
            classes.append('bid__item--owned')
        
        best_bid_list.append({
            'total_price': bid.total_price,
            'str_class': " ".join(classes),
        })
    
    return best_bid_list
    



def get_online_context(offer_id, answer_id):
    
    offer = get_object_or_404(AhOffer, id=offer_id)
    answer = get_object_or_404(AhAnswer, id=answer_id)
    
    lines_object = []
    for line in answer.my_lines.all():
        lines_object.append({
            'ah_a_line': line,
            'str_class': 'bid__item--best' if is_best_line(line) else '',
        })
    
    best_bids = offer.answers.order_by('-total_price')[:5]
    ordered_best_bid_list = get_classed_best_bids(best_bids, answer_id)
    
    str_arriv = arrival_type_of_realtime_auction(offer)
    
    context = {
        'offer': offer, 'object': answer,
        'answer': answer,
        'customer': answer.owner,
        'arrival': str_arriv,
        
        'content_header': {
            'title': offer.description,
            'desc': _("Online auction"),
        },
        
        'ordered_best_bid_list': ordered_best_bid_list,
        'lines': lines_object,
    }
    return context




def get_online_info_context(offer_id):
    
    offer = get_object_or_404(AhOffer, id=offer_id)
    
    best_bids = offer.answers.all().order_by('-total_price')[:5]
    ordered_best_bid_list = get_classed_best_bids(best_bids)
    
    str_arriv = arrival_type_of_realtime_auction(offer)
    
    context = {
        'offer': offer, 'object': offer,
        'customer': offer.owner,
        'arrival': str_arriv,
        
        'content_header': {
            'title': offer.description,
            'desc': _("Online auction info"),
        },
        
        'ordered_best_bid_list': ordered_best_bid_list,
    }
    return context




def answer_update_ppu(answer_line):
    answer_line.total_price = answer_line.ppu * answer_line.offer_line.amount
    answer_line.save()
    answer_line.answer.refresh_total_price()
    return


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
    context = ntf_manager.NtfContext()
    context['place'] = place
    context['item'] = item
    send_ntf_from_state(request, state, context)
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
    context = ntf_manager.NtfContext()
    context['place'] = place
    context['offer_description'] = offer_description
    if set_url != "":
        context['access_url'] = set_url
    ntf_manager.send_by_template(request, context, customer, template, admins, business)

def ntf_create_from_auction(
    template='fallback',
    context=None,
    cust_url='Not set',
    customer=None,
    admins=False,
    business=False,
    ):
    message = ntf_manager.NtfMessage()
    message.template = template
    message.context = context
    message.context['access_url'] = cust_url
    message = customer.add_emails(message, False, True)
    return message
