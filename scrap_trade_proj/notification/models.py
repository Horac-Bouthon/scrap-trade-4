from django.db import models
from translatable.models import TranslatableModel, get_translation_model
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

# Create your models here.
BODY_TYPES_CHOICES = [
    ('text', 'Text'),
    ('html', 'Html'),
]

class NtfSetup(models.Model):
    serve_email = models.BooleanField(
        default=True,
        verbose_name=_('Send emails'),
        help_text=_("Can send emails.")
    )
    serve_sms = models.BooleanField(
        default=False,
        verbose_name=_('Send SMS'),
        help_text=_("Can send SMS.")
    )
    smtp_url = models.CharField(
        verbose_name=_('Smtp addrerss'),
        help_text=_("URL to connect to SMTP server."),
        max_length=100,
        null=True,
        blank=True,
        unique=False,
    )
    smtp_port = models.IntegerField(
        verbose_name=_('Smtp port'),
        help_text=_("Port to connect to SMTP server."),
        null=True,
        blank=True,
        unique=False,
    )
    smtp_ssl = models.BooleanField(
        default=False,
        verbose_name=_('Connect SSL'),
        help_text=_("Use SSL connection.")
    )
    sender_user = models.CharField(
        max_length=100,
        verbose_name=_('Smtp user'),
        help_text=_("User to connect SMTP server."),
        null=True,
        blank=True,
    )
    sender_password = models.CharField(
        max_length=50,
        verbose_name=_('Smtp user password'),
        help_text=_("User password to connect SMTP server."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('NtfSetup definition', 'NtfSetup')
        verbose_name_plural = tr.pgettext_lazy('NtfSetup definition', 'NtfSetup')

    def __str__(self):
        return "serve_email={},serve_sms={},smtp_url='{}',smtp_port={},smtp_ssl={},sender_user='{}',sender_password='{}'"\
            .format(self.serve_email, self.serve_sms, self.smtp_url,\
            self.smtp_port, self.smtp_ssl, self.sender_user,\
            self.sender_password)


class MessTemp(TranslatableModel):
    temp_key = models.CharField(
        max_length=20,
        default="fallback",
        verbose_name=tr.pgettext_lazy('MessTemp definition', 'Template key'),
        help_text=tr.pgettext_lazy('MessTemp definition','Key to identify the template'),
        null=True,
        blank=True,
    )
    temp_type = models.CharField(
        max_length=10,
        choices=BODY_TYPES_CHOICES,
        default="text",
        verbose_name=tr.pgettext_lazy('MessTemp definition', 'Template type'),
        help_text=tr.pgettext_lazy('MessTemp definition','Template type (text/html)'),
        null=True,
        blank=True,
    )


    class Meta:
        verbose_name = tr.pgettext_lazy('MessTemp definition', 'Message Template')
        verbose_name_plural = tr.pgettext_lazy('MessTemp definition', 'Message Templates')

    def __str__(self):
        return self.temp_key

    def get_act_subject(self):
        return self.get_subject_by_code(tr.get_language())

    def get_act_body(self):
        return self.get_body_by_code(tr.get_language())

    def get_subject_by_code(self, lan_code):
        return self.translated('subject', default=None, language=lan_code, fallback=True)

    def get_body_by_code(self, lan_code):
        return self.translated('body', default=None, language=lan_code, fallback=True)


class MessTempTranslation(get_translation_model(MessTemp, "messtemp")):
    subject = models.CharField(
        verbose_name=_('Subject'),
        help_text=_("Message subject."),
        max_length=200,
        null=True,
        blank=True,
        unique=False
    )
    body =  models.TextField(
        verbose_name=_('Body'),
        help_text=_("Message body (playn-text/html)."),
        null=True,
        blank=True,
        unique=False,
    )
