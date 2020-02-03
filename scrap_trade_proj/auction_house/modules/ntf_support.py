from auction_house.models import (
    AhOffer,
    AhAnswer,
)
from project_main.models import Project

from notification.modules import ntf_manager

from django.urls import reverse
from django.template import Context
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr
from customers.modules.ntf_support import add_poweruser_to_ntf
from notification.modules.ntf_support import (
    clone_context,
    send_via_ntf,
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
    #--- offer_confirmed
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
        ret_val = send_via_ntf(request, mess_list, f_context)
    #---- answer_successful
    if state.state_key == 'answer_successful':
        if type(item).__name__ != 'AhAnswer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-answer-detail', args=[item.pk]))
        message = ntf_manager.NtfMessage()
        message.template = state.ntf_template
        message.context = clone_context(context)
        message.context['access_url'] = cust_url
        message.reciver_list.clear()
        message = customer.add_emails(message, False, True)
        ret_val = send_via_ntf(request, message, f_context)
    #---- offer_accepted
    if state.state_key == 'offer_accepted':
        if type(item).__name__ != 'AhOffer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-offer-detail', args=[item.pk]))
        message = ntf_manager.NtfMessage()
        message.template = state.ntf_template
        message.context = clone_context(context)
        message.context['access_url'] = cust_url
        message.reciver_list.clear()
        message = customer.add_emails(message, False, True)
        ret_val = send_via_ntf(request, message, f_context)
    #---- offer_ready_to_close
    if state.state_key == 'offer_ready_to_close':
        if type(item).__name__ != 'AhOffer':
            return False
        customer = item.owner
        cust_url = request.build_absolute_uri(reverse('ah-offer-detail', args=[item.pk]))
        message = ntf_manager.NtfMessage()
        message.template = state.ntf_template
        message.context = clone_context(context)
        message.context['access_url'] = cust_url
        message.reciver_list.clear()
        message = customer.add_emails(message, False, True)
        ret_val = send_via_ntf(request, message, f_context)
    return ret_val
