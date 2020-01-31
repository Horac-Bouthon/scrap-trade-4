import smtplib
from django.conf import settings
from notification.models import NtfSetup

from email.message import EmailMessage

def send(obj):
    print('email.send')
    notification = NtfSetup.objects.all().first()
    EMAIL_ADDRESS = notification.sender_user
    EMAIL_PASSWORD = notification.sender_password
    SMTP_ADDRESS = notification.smtp_url
    SMTP_PORT = notification.smtp_port

    try:
        if notification.smtp_ssl:
            with smtplib.SMTP_SSL(str(SMTP_ADDRESS), SMTP_PORT) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                if type(obj).__name__ == 'list':
                    for message in obj:
                        send_one_msg(smtp, message)
                if type(obj).__name__ == 'NtfMessage':
                    send_one_msg(smtp, obj)
        else:
            print('only smpt')
            with smtplib.SMTP(str(SMTP_ADDRESS), SMTP_PORT) as smtp:
                # debuging with smtpd (https://pymotw.com/2/smtpd/)
                if EMAIL_ADDRESS != 'no_login':
                    smtp.ehlo()
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                print('obj type = {}'.format(type(obj).__name__))
                if type(obj).__name__ == 'list':
                    for message in obj:
                        send_one_msg(smtp, message)
                if type(obj).__name__ == 'NtfMessage':
                    send_one_msg(smtp, obj)
    except:
        return False
    return True

def send_one_msg(server, obj_message):
    print('send_one_msg')
    for lang in settings.LANGUAGES:
        print('lang = {}'.format(lang))
        if len(lang) == 2:
            if send_by_lang(server, obj_message, lang[0]):
                break

def send_by_lang(server, obj_message, lang_code='en'):
    print('send_by_lang({})'.format(lang_code))

    print('obj_message(1) = {}'.format(repr(obj_message)))
    if obj_message.template != "":
        obj_message.set_from_template(lang_code)
    obj_message.render_str_template()
    print('obj_message(2) = {}'.format(repr(obj_message)))

    contacts = list()
    print('reciver_list = {}'.format(obj_message.reciver_list))
    for reciver in obj_message.reciver_list:
        if reciver[1] == lang_code:
            contacts.append(reciver[0])
    print('contacts = {}'.format(contacts))


    if obj_message.sender == "":
        notification = NtfSetup.objects.all().first()
        obj_message.sender = notification.sender_user

    if len(contacts) < 1:
        return False

    msg = EmailMessage()
    msg['Subject'] = obj_message.subject
    msg['From'] = obj_message.sender
    if obj_message.body_type == 'text':
        msg.set_content(obj_message.body)
    if obj_message.body_type == 'html':
        msg.add_alternative(obj_message.body, subtype='html')
    print('before send')
    if not obj_message.is_mail_list:
        for receiver in contacts:
            msg['To'] = receiver
            server.send_message(msg)
    else:
        msg['To'] = ', '.join(contacts)
        server.send_message(msg)
    print('after send')
    return True
