from notification.modules import email
from notification.models import NtfSetup, MessTemp
from django.utils import translation as tr
from django.template import Context
from django.template import Template

class NtfMessage:

    def __init__(self,
            m_type='email',
            subject='message subject',
            body_type='text',
            body="",
            context=Context(),
            sender="",
            reciver_list=None,
            is_mail_list=False,
            ):
        self.m_type = m_type.lower()
        self.subject = subject
        self.body_type = body_type
        self.body = body
        self.context = context
        self.sender = sender
        self.reciver_list=reciver_list
        if reciver_list != None:
            self.reciver_list=reciver_list
        else:
            self.reciver_list=list()
        self.is_mail_list = is_mail_list

    def __repr__(self):
        return "NtfMessage('{}', '{}', '{}', '{}', {}, '{}', {}, {})"\
            .format(self.m_type, self.subject, self.body_type,\
            self.body, self.context, self.sender,\
            self.reciver_list, self.is_mail_list)

    def __str__(self):
        return "message-{}/{}"\
            .format(self.m_type, self.subject)

    def render_str_template(self):
        template = Template(self.subject)
        self.subject = template.render(self.context)
        template = Template(self.body)
        self.body = template.render(self.context)

    def set_from_template(self, temp_key='fallback', lan_code='en'):
        temp_data = MessTemp.objects.get(temp_key = temp_key)
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
            return self.set_from_template('fallback',lan_code)
        return False


def send(ntf_message_man):
    notification = NtfSetup.objects.all().first()
    ret_val = True
    if notification.serve_email:
        ret_val = email.send(ntf_message_man)
    return ret_val
