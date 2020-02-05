from notification.modules import email
from notification.models import NtfSetup, MessTemp
from django.utils import translation as tr
from django.template import Context
from django.template import Template
from project_main.models import Project
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr
from customers import models as mc


#--------------------  clases
class NtfContext(Context):
    def clone_context(self):
        clone = NtfContext()
        for dict_i in self:
            for key in dict_i:
                clone[key] = self[key]
        return clone


class NtfMessage:

    def __init__(self,
            m_type='email',
            subject='message subject',
            body_type='text',
            body="",
            template="",
            context=NtfContext(),
            sender="",
            reciver_list=None,
            is_mail_list=False,
            ):
        self.m_type = m_type.lower()
        self.subject = subject
        self.body_type = body_type
        self.body = body
        self.template = template
        self.context = context
        self.sender = sender
        self.reciver_list=reciver_list
        if reciver_list != None:
            self.reciver_list=reciver_list
        else:
            self.reciver_list=list()
        self.is_mail_list = is_mail_list

    def __repr__(self):
        return "NtfMessage('{}', '{}', '{}', '{}', '{}', {}, '{}', {}, {})"\
            .format(self.m_type, self.subject, self.body_type,\
            self.body, self.template, self.context, self.sender,\
            self.reciver_list, self.is_mail_list)

    def __str__(self):
        return "message-{}/{}"\
            .format(self.m_type, self.subject)

    def render_str_template(self):
        template = Template(self.subject)
        self.subject = template.render(self.context)
        template = Template(self.body)
        self.body = template.render(self.context)

    def set_from_template(self, lan_code='en'):
        temp_data = MessTemp.objects.get(temp_key = self.template)
        if not temp_data is None:
            self.body_type = temp_data.temp_type
            if lan_code is None or lan_code == "":
                self.subject = temp_data.get_act_subject()
                self.body = temp_data.get_act_body()
            else:
                self.subject = temp_data.get_subject_by_code(lan_code)
                self.body = temp_data.get_body_by_code(lan_code)
            return True
        else:
            self.template = 'fallback'
            return self.set_from_template(lan_code)
        return False

    def clone_me(self):
        new_obj = NtfMessage(
            m_type=self.m_type,
            subject=self.subject,
            body_type=self.body_type,
            body=self.body,
            template=self.template,
            context=self.context,
            sender=self.sender,
            reciver_list=self.reciver_list,
            is_mail_list=self.is_mail_list,
        )
        return new_obj

#-------------------------------- functions`
def send_via_ntf(request, object, fail_context):
    fail_context['orig'] = repr(object)
    if not send(object):
        allert_poweruser_ntf_failure(request, fail_context)

def send_by_template_to_address(request, context, address_obj, temp_key):
    context['app_name'] = Project.objects.all().first().project_name
    f_context = context.clone_context()
    message = NtfMessage()
    message.template = temp_key
    message.context = context
    message.reciver_list.append(address_obj)
    ret_val = send_via_ntf(request, message, f_context)
    return

def send(ntf_message_man):
    notification = NtfSetup.objects.all().first()
    ret_val = True
    if notification.serve_email:
        ret_val = email.send(ntf_message_man)
    return ret_val

def allert_poweruser_ntf_failure(request, context):
    context['app_name'] = Project.objects.all().first().project_name
    context['url'] = request.build_absolute_uri()
    context['user_mail'] = request.user.email
    if request.user.customer is None:
        context['user_cust'] = _('Not set')
    else:
        context['user_cust'] = request.user.customer.customer_name

    message = NtfMessage()
    message.template = 'ntf_failur'
    message.context = context
    message.reciver_list.clear()
    message = add_poweruser_to_ntf(message)
    send(message)
    return

def send_by_template(request, context, customer, temp_key, admin, business):
    context['app_name'] = Project.objects.all().first().project_name
    f_context = context.clone_context()
    message = NtfMessage()
    message.template = temp_key
    message.context = context
    message = customer.add_emails(message, admin, business)
    ret_val = send_via_ntf(request, message, f_context)
    return

def add_poweruser_to_ntf(ntf_message):
    for user in mc.ProjectCustomUser.objects.all():
        if user.has_perm("customers.is_poweruser"):
            ntf_message.reciver_list.append((user.email, user.userprofile.language))
    return ntf_message
