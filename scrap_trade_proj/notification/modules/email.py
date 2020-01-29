import smtplib
from notification.models import NtfSetup

from email.message import EmailMessage

def send(obj_message):

    notification = NtfSetup.objects.all().first()
    obj_message.render_str_template()

    EMAIL_ADDRESS = notification.sender_user
    EMAIL_PASSWORD = notification.sender_password
    SMTP_ADDRESS = notification.smtp_url
    SMTP_PORT = notification.smtp_port

    contacts = obj_message.reciver_list

    if obj_message.sender == "":
        obj_message.sender = EMAIL_ADDRESS

    if len(contacts) < 1:
        return False

    msg = EmailMessage()
    msg['Subject'] = obj_message.subject
    msg['From'] = obj_message.sender
    if obj_message.is_mail_list:
        msg['To'] = ', '.join(contacts)
    if obj_message.body_type == 'text':
        msg.set_content(obj_message.body)
    if obj_message.body_type == 'html':
        msg.add_alternative(obj_message.body, subtype='html')
    try:
        if notification.smtp_ssl:
            print('smtp_address={} / smtp_port={}'.format(SMTP_ADDRESS, SMTP_PORT))
            with smtplib.SMTP_SSL(str(SMTP_ADDRESS), SMTP_PORT) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                if not obj_message.is_mail_list:
                    for receiver in contacts:
                        msg['To'] = receiver
                        smtp.send_message(msg)
                else:
                    msg['To'] = ', '.join(contacts)
                    smtp.send_message(msg)
        else:
            print('message={}'.format(repr(obj_message)))
            with smtplib.SMTP(str(SMTP_ADDRESS), SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                if not obj_message.is_mail_list:
                    for receiver in contacts:
                        msg['To'] = receiver
                        smtp.send_message(msg)
                else:
                    msg['To'] = ', '.join(contacts)
                    smtp.send_message(msg)
    except:
        return False
    return True
