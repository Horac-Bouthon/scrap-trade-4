from django.db import models
from django.conf import settings
from django.urls import reverse

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from translatable.models import TranslatableModel, get_translation_model

from project_main.models import Project

from auction_house.models import AhOffer, AhAnswer

from customers.models import (
    ProjectCustomUser,
)


# Create your models here.

class StepState(TranslatableModel):
    state_key = models.CharField(
        max_length=50,
        default="state",
        verbose_name=tr.pgettext_lazy('StepState definition', 'State'),
        help_text=tr.pgettext_lazy('StepState definition','State'),
        null=True,
        blank=True,
    )
    previous = models.ManyToManyField(
        'StepState',
        verbose_name=tr.pgettext_lazy('StepState definition', 'Previous'),
        help_text=tr.pgettext_lazy('StepState definition','Previous state'),
        related_name="next_states",
        blank=True,
    )
    security_level = models.IntegerField(
        verbose_name=_('Security level'),
        help_text=_("Abstract security level"),
        default = 0,
    )
    group_key = models.IntegerField(
        default=1,
        verbose_name=_('Group'),
        help_text=_("Key for the division of states into groups. ")
    )
    group_serial_number = models.IntegerField(
        default=0,
        verbose_name=_('Serial number'),
        help_text=_("Serial number inside the group. ")
    )
    manual_set = models.BooleanField(
        default=False,
        verbose_name=_('Manual set'),
        help_text=_("State change manually.")
    )
    is_alert_button = models.BooleanField(
        default=False,
        verbose_name=_('Alert button'),
        help_text=_("Show starting button like alert. ")
    )


    class Meta:
        verbose_name = tr.pgettext_lazy('StepState definition', 'State')
        verbose_name_plural = tr.pgettext_lazy('StepState definition', 'States')

    def __str__(self):
        return self.act_state_name()

    def act_state_name(self):
        lang = tr.get_language()
        return self.translated('state_name', default=None, language=lang, fallback=True)

    def get_state_name_plural(self):
        lang = tr.get_language()
        return self.translated('state_name_plural', default=None, language=lang, fallback=True)

    def get_actual_state_button(self):
        lang = tr.get_language()
        return self.translated('state_button_text', default=None, language=lang, fallback=True)

    def get_actual_template_title(self):
        lang = tr.get_language()
        return self.translated('state_template_title', default=None, language=lang, fallback=True)

    def get_actual_template_question(self):
        lang = tr.get_language()
        return self.translated('state_template_question', default=None, language=lang, fallback=True)

    def get_actual_template_text(self):
        lang = tr.get_language()
        return self.translated('state_template_text', default=None, language=lang, fallback=True)

    def get_actual_confirm_button(self):
        lang = tr.get_language()
        return self.translated('state_template_confitm_button', default=None, language=lang, fallback=True)

    def get_actual_cancel_button(self):
        lang = tr.get_language()
        return self.translated('state_template_cancel_button', default=None, language=lang, fallback=True)

    @staticmethod
    def get_group_members(par_group_key):
        return StepState.objects.filter(group_key = par_group_key).order_by('group_serial_number')

class StepStateTranslation(get_translation_model(StepState, "stepstate")):
    state_name = models.CharField(
        verbose_name=_('State name'),
        help_text=_("Display name of state."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
    )
    state_name_plural = models.CharField(
        verbose_name=_('State name plural'),
        help_text=_("Display name of state in plural."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
    )
    state_description = models.CharField(
        verbose_name=_('State description'),
        help_text=_("Short description."),
        max_length=100,
        null=True,
        blank=True,
        unique=False
        )
    state_button_text = models.CharField(
        verbose_name=_('State button text'),
        help_text=_("Activating button text."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
        )
    state_template_title = models.CharField(
        verbose_name=_('State template title'),
        help_text=_("Template title text."),
        max_length=200,
        null=True,
        blank=True,
        unique=False
        )
    state_template_question =  models.TextField(
        verbose_name=_('State template question'),
        help_text=_("Template text to query state change."),
        null=True,
        blank=True,
        unique=False,
    )
    state_template_text =  models.TextField(
        verbose_name=_('State template text'),
        help_text=_("Text to describe the state change."),
        null=True,
        blank=True,
        unique=False,
    )
    state_template_confitm_button = models.CharField(
        verbose_name=_('State template confirm button'),
        help_text=_("Template state confirmation button text."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
        )
    state_template_cancel_button = models.CharField(
        verbose_name=_('State template cancel button'),
        help_text=_("Template state cancel button text."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
        )


class Step(models.Model):
    state = models.ForeignKey(
        StepState,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('Step definition', 'State'),
        help_text=tr.pgettext_lazy('Step definition','Link to step state'),
        related_name="steps",
        null=True,
    )
    offer_link = models.ForeignKey(
        AhOffer,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('Step definition', 'Offer'),
        help_text=tr.pgettext_lazy('Step definition','Link to offer'),
        related_name="my_steps",
        null=True, blank=True,
    )
    answer_link = models.ForeignKey(
        AhAnswer,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('Step definition', 'Answer'),
        help_text=tr.pgettext_lazy('Step definition','Link to answer'),
        related_name="my_steps",
        null=True, blank=True,
    )
    changed_by = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('Step definition', 'Created by'),
        help_text=tr.pgettext_lazy('Step definition','Link to creator'),
        null=True, blank=True,
        related_name="my_steps",
    )
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = tr.pgettext_lazy('Step definition', 'Step')
        verbose_name_plural = tr.pgettext_lazy('Step definition', 'Steps')

    def __str__(self):
        return '{} {} {} {} {}'.format(self.pk,
            self.state.act_state_name(),
            self.offer_link,
            self.answer_link,
            self.created_at,
        )
