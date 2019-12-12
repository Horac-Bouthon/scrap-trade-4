from auction_house.models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
    AhAnswerLine
)

from customers.models import (
    Customer,
)
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from datetime import date
from datetime import datetime

def resurect_auction(par_offer):
    print('resurect offer: {}'.format(par_offer))
    par_offer.is_new = False
    par_offer.is_confirmed = True
    par_offer.is_accepted = False
    par_offer.is_ready_close = False
    par_offer.is_closed = False
    par_offer.is_cancelled = False
    par_offer.save()
    for set_a in par_offer.answers.filter(is_cancelled = False):
        print('resurect answer: {}'.format(set_a))
        set_a.is_new = False
        set_a.is_confirmed = True
        set_a.is_accepted = False
        set_a.is_closed = False
        set_a.is_successful = False
        set_a.is_cancelled = False
        set_a.changed_by = None
        set_a.save()
    return

def set_auction(par_offer):
    print('from second: {} must be set / {}'.format(par_offer, par_offer.auction_date))
    # kill not confirmed Answers
    new_answers = par_offer.answers.filter(is_new = True)
    for kill_answer in new_answers:
        print('kill answer = {}'.format(kill_answer))
        kill_answer.is_new = False
        kill_answer.is_confirmed = False
        kill_answer.is_accepted = False
        kill_answer.is_bound = False
        kill_answer.is_closed = False
        kill_answer.is_successful = False
        kill_answer.is_cancelled = True
        kill_answer.canceled_at = datetime.now()
        kill_answer.changed_by = None
        kill_answer.save()
    my_answers = par_offer.answers.filter(is_confirmed = True)
    if my_answers.count() > 0 :
        # vyhodnoceni
        print('vyhodnoceni {}'.format(par_offer))
        # find and mark succesfull
        lucky_one = my_answers.all().order_by('-total_price').first()
        print('set to {}'.format(lucky_one))
        lucky_one.is_new = False
        lucky_one.is_confirmed = False
        lucky_one.is_accepted = False
        lucky_one.is_bound = True
        lucky_one.is_closed = False
        lucky_one.is_successful = True
        lucky_one.is_cancelled = False
        lucky_one.changed_by = None
        lucky_one.save()
        # unbound others
        for unlucky_one in my_answers.filter(is_bound = False):
            print('close {}'.format(unlucky_one))
            unlucky_one.is_new = False
            unlucky_one.is_confirmed = False
            unlucky_one.is_accepted = False
            unlucky_one.is_bound = False
            unlucky_one.is_closed = True
            unlucky_one.is_successful = False
            unlucky_one.is_cancelled = False
            unlucky_one.closed_at = datetime.now()
            unlucky_one.changed_by = None
            unlucky_one.save()

    else:
        # cancel offer - no anwers
        print('cancel - no answers - {}'.format(par_offer))
        # kill offer
        par_offer.is_new = False
        par_offer.is_confirmed = False
        par_offer.is_accepted = False
        par_offer.is_ready_close = False
        par_offer.is_closed = False
        par_offer.is_cancelled = True
        par_offer.canceled_at = datetime.now()
        par_offer.save()


def make_auctions(par_ref_dt):
    dt_ref = parse_datetime(par_ref_dt)
    if not is_aware(dt_ref):
        dt_ref = make_aware(dt_ref)
    print('make auction at {}'.format(dt_ref))
    my_offers = AhOffer.objects.filter(is_confirmed = True)
    for offer in my_offers:
        auction_dt = datetime.combine(offer.auction_date, datetime.min.time())
        if not is_aware(auction_dt):
            auction_dt = make_aware(auction_dt)
        if auction_dt <= dt_ref:
            set_auction(offer)
        else:
            print('{} is waiting / {}'.format(offer, offer.auction_date))
