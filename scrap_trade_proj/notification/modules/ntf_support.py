from project_main.models import Project

from notification.modules import ntf_manager

from django.urls import reverse
from django.template import Context
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr


def send_via_ntf(request, object, fail_context):
    fail_context['orig'] = repr(object)
    if not ntf_manager.send(object):
        allert_poweruser_ntf_failure(request, fail_context)

def allert_poweruser_ntf_failure(request, context):
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

def send_by_template_to_address(request, context, address_obj, temp_key):
    context['app_name'] = Project.objects.all().first().project_name
    f_context = clone_context(context)
    message = ntf_manager.NtfMessage()
    message.template = temp_key
    message.context = context
    message.reciver_list.append(address_obj)
    ret_val = send_via_ntf(request, message, f_context)
    return

#-----------------------------------------------------------------------------
def clone_context(source):
    clone = Context()
    for dict_i in source:
        for key in dict_i:
            clone[key] = source[key]
    return clone
