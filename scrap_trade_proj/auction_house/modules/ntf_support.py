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
from project_main.models import Project

from notification.modules import ntf_manager

from django.urls import reverse
from django.template import Context
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from customers.models import (
    Customer,
    ProjectCustomUser,
)

def send_ntf_from_state(request, state, context):
    f_context = clone_context(context)
    #--- settings
    ret_val = True
    if 'item' in context:
        item = context['item']
    else:
        item = None
    #--- set context
    context['app_name'] = Project.objects.all().first().project_name
    #--- state depending
    if state.state_key == 'offer_confirmed':
        if type(item).__name__ != 'AhOffer':
            return False
        mess_list = list()
        for customer in item.offered_to.all():
            cust_url = request.build_absolute_uri(reverse('ah-customer-answers-create', args=[customer.pk, item.pk]))
            message = ntf_manager.NtfMessage()
            message.template = state.ntf_template
            message.context = clone_context(context)
            message.context['access_url'] = cust_url
            message.reciver_list.clear()
            message = customer.add_emails(message, False, True)
            mess_list.append(message)
        print("ml = {}".format(mess_list))
        ret_val = send_via_ntf(request, mess_list, f_context)
    return ret_val

def clone_context(source):
    clone = Context()
    for dict_i in source:
        for key in dict_i:
            clone[key] = source[key]
    return clone

def send_via_ntf(request, object, fail_context):
    fail_context['orig'] = repr(object)
    if not ntf_manager.send(object):
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
    message.template = 'ntf_failur'
    message.context = context
    message.reciver_list.clear()
    message = add_poweruser_to_ntf(message)
    ntf_manager.send(message)
    return

def add_poweruser_to_ntf(ntf_message):
    for user in ProjectCustomUser.objects.all():
        if user.has_perm("customers.is_poweruser"):
            ntf_message.reciver_list.append((user.email, user.userprofile.language))
    return ntf_message
