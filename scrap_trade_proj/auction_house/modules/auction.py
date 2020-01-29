from auction_house.models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
    AhAnswerLine
)

from state_wf.models import (
    Step,
    StepState,
)
from notification.modules import ntf_manager

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from customers.models import (
    Customer,
    ProjectCustomUser,
)
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from datetime import date
from datetime import datetime


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

def set_auction(par_offer):
    print('from second: {} must be set / {}'.format(par_offer, par_offer.auction_date))
    # kill not confirmed Answers
    state_obj = StepState.objects.get(state_key='answer_canceled')
    new_answers = fiter_by_state(par_offer.answers, 'answer_new')
    for kill_answer in new_answers:
        print('kill answer = {}'.format(kill_answer))
        answer_add_state(kill_answer, state_obj, None)
    my_answers = fiter_by_state(par_offer.answers, 'answer_confirmed')
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
        # unbound others
        state_obj = StepState.objects.get(state_key='answer_closed')
        for unlucky_one in fiter_by_state(par_offer.answers, 'answer_confirmed'):
            print('close {}'.format(unlucky_one))
            answer_add_state(unlucky_one, state_obj, None)
    else:
        # cancel offer - no anwers
        print('cancel - no answers - {}'.format(par_offer))
        # kill offer
        state_obj = StepState.objects.get(state_key='offer_canceled')
        offer_add_state(par_offer, state_obj, None)


def make_auctions(par_ref_dt):
    dt_ref = parse_datetime(par_ref_dt)
    if not is_aware(dt_ref):
        dt_ref = make_aware(dt_ref)
    print('make auction at {}'.format(dt_ref))
    my_offers = fiter_by_state(AhOffer.objects.all(), 'offer_confirmed')
    for offer in my_offers:
        auction_dt = datetime.combine(offer.auction_date, datetime.min.time())
        if not is_aware(auction_dt):
            auction_dt = make_aware(auction_dt)
        if auction_dt <= dt_ref:
            set_auction(offer)
        else:
            print('{} is waiting / {}'.format(offer, offer.auction_date))

#-------------------------------- offer views
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

def fiter_by_state(p_data, p_state_key):
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

def customer_answer_create(customer, offer, user, data):
    new = AhAnswer(
        description = data['description'],
        owner = customer,
        ah_offer = offer,
        creator = user,
        changed_by = user,
    )
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
    #ret_offers = par_customer.receive_offers.filter(is_confirmed = True)
    ret_offers = fiter_by_state(par_customer.receive_offers.all(), 'offer_confirmed')
    for answer in par_customer.owned_answers.all():
        ret_offers = ret_offers.exclude(id = answer.ah_offer.pk)
    return ret_offers.order_by("-pk")

def get_auction_list_control_obj(customer, data_offer, data_answers):
    ret_val = list()
    offer_list = list()
    for state in StepState.get_group_members(1):
        obj_line = AuctionLine(
            state.get_state_name_plural(),
            fiter_by_state(data_offer, state.state_key).count(),
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
            fiter_by_state(data_answers, state.state_key).count(),
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

def send_via_ntf(request, ntf_message, fail_context):
    if not ntf_manager.send(ntf_message):
        fail_context['orig'] = repr(ntf_message)
        allert_poweruser_ntf_failure(request, fail_context)



def allert_poweruser_ntf_failure(request, context):
    print('allert_poweruser_ntf_failure')
    context['url'] = request.build_absolute_uri()
    context['user_mail'] = request.user.email
    if request.user.customer is None:
        context['user_cust'] = _('Not set')
    else:
        context['user_cust'] = request.user.customer.customer_name

    message = ntf_manager.NtfMessage()
    message.set_from_template('ntf_failur','en')
    message.context = context
    message.reciver_list.clear()
    message = add_poweruser_to_ntf(message)
    ntf_manager.send(message)
    return


def add_poweruser_to_ntf(ntf_message):
    for user in ProjectCustomUser.objects.all():
        if user.has_perm("customers.is_poweruser"):
            ntf_message.reciver_list.append(user.email)
    return ntf_message

def add_admin_from_customer_to_ntf(ntf_message, customer):
    for user in customer.projectcustomuser_set.all():
        if user.has_perm("customers.is_customer_admin"):
            ntf_message.reciver_list.append(user.email)
    for email in customer.customeremail_set.all():
        if user.is_admin_adr:
            ntf_message.reciver_list.append(email.customer_email)
    return ntf_message
