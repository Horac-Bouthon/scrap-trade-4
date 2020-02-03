from project_main.models import Project

from notification.modules import ntf_manager

from django.urls import reverse
from django.template import Context
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr
from notification.modules.ntf_support import (
    clone_context,
    send_via_ntf,
)

from project_main.models import Project
from customers.models import (
    Customer,
    ProjectCustomUser,
)

def send_by_template(request, context, customer, temp_key, admin, business):
    context['app_name'] = Project.objects.all().first().project_name
    f_context = clone_context(context)
    message = ntf_manager.NtfMessage()
    message.template = temp_key
    message.context = context
    message = customer.add_emails(message, admin, business)
    ret_val = send_via_ntf(request, message, f_context)
    return

def add_poweruser_to_ntf(ntf_message):
    for user in ProjectCustomUser.objects.all():
        if user.has_perm("customers.is_poweruser"):
            ntf_message.reciver_list.append((user.email, user.userprofile.language))
    return ntf_message
