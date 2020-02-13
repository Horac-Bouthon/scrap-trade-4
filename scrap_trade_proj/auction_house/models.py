from django.db import models
from datetime import datetime
from django import forms
from customers.models import (
    Customer,
    ProjectCustomUser,
)
from integ.models import OpenId

from django.conf import settings
from django.urls import reverse

from translatable.models import TranslatableModel, get_translation_model

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

#------------------------  AhOffer
class AhOffer(models.Model):
    description = models.CharField(
        max_length=200,
        verbose_name=_('Description'),
        help_text=_("Offers description"),
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Owner'),
        help_text=tr.pgettext_lazy('AhOffer definition','Link to Owner'),
        related_name="owned_offers",
        null=True,
    )
    creator = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Creator'),
        help_text=tr.pgettext_lazy('AhOffer definition','Link to Creator'),
        related_name="created_offers",
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Created at'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of offer creation'),
        auto_now_add=True,
    )
    changed_by = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Last change'),
        help_text=tr.pgettext_lazy('AhOffer definition','Link to user made last change'),
        null=True, blank=True,
        related_name="last_changed_offers",
    )
    changed_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Changed at'),
        auto_now=True,
    )
    offered_to = models.ManyToManyField(
        Customer,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Offered to'),
        help_text=tr.pgettext_lazy('AhOffer definition','List of customers who recieved the offer'),
        related_name="recieve_offers",
        blank=True,
    )
    auction_date = models.DateField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Auction date'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of auction'),
        null=True,
        blank=True,
    )
    delivery_date = models.DateField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Delivery date'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of the delivery'),
        null=True,
        blank=True,
    )
    minimal_total_price =  models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Minimal total price'),
        help_text=tr.pgettext_lazy('AhOffer definition','Final minimal price'),
        null=True,
        blank=True,
    )
    auction_url = models.URLField(
        max_length=200,
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Auction URL'),
        help_text=tr.pgettext_lazy('AhOffer definition','Online auction url'),
        null=True,
        blank=True,
    )
    auction_start = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Auction start'),
        help_text=tr.pgettext_lazy('AhOffer definition','From this time is auction URL accessible'),
        null=True,
        blank=True,
    )
    auction_end = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Auction end'),
        help_text=tr.pgettext_lazy('AhOffer definition','From this time is auction URL closed'),
        null=True,
        blank=True,
    )
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_offers',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhOffer definition', 'Offer')
        verbose_name_plural = tr.pgettext_lazy('AhOffer definition', 'Offers')

    def get_absolute_url(self):
        return reverse('ah-offer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} ({}) {}'.format(self.pk, self.owner.customer_name, self.description, self.created_at)

    @property
    def actual_state(self):
        steps = self.my_steps.all().order_by("-created_at")
        if steps.count() > 0:
            return steps.first().state
        return None

    def is_equal_state(self, state):
        return (self.actual_state == state)

    def get_steps(self):
        return self.my_steps.all().order_by("-created_at")

    def refresh_total_price(self):
        total = 0
        for line in self.lines.all():
            total = total + (line.amount * line.minimal_ppu)
        self.minimal_total_price = total
        self.save()


#------------------------  AhOfferLine
class AhOfferLine(models.Model):
    description = models.CharField(
        max_length=200,
        verbose_name=_('Description'),
        help_text=_("Offers line description"),
    )
    amount =  models.DecimalField(
        max_digits = 10,
        decimal_places = 4,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Amount'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Quantity of material'),
    )
    offer = models.ForeignKey(
        'AhOffer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Offer'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Link to Offer'),
        related_name="lines",
    )
    mat_class = models.ForeignKey(
        'AhMatClass',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Material class'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Link to Material class'),
        related_name="used_lines",
    )
    minimal_ppu =  models.DecimalField(
        max_digits = 7,
        decimal_places = 2,
        default=0.0,
        verbose_name=tr.pgettext_lazy('AhAnswerLine definition', 'Minimal price per unit'),
        help_text=tr.pgettext_lazy('AhAnswerLine definition','Minimal price for one measurement unit'),
    )
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_offer_lines',
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhOffer definition', 'Offer line')
        verbose_name_plural = tr.pgettext_lazy('AhOffer definition', 'Offer lines')

    def get_absolute_url(self):
        return reverse('ah-offer-detail', kwargs={'pk': self.offer.pk})

    def __str__(self):
        return '{} - {} from {} - {} '.format(self.pk, self.description, self.offer.pk, self.offer.description)


#------------------------  AhMatClass
class AhMatClass(TranslatableModel):
    class_name = models.CharField(
        max_length=200,
        verbose_name=_('Material class name'),
        help_text=_("Name of the material class"),
        unique = True,
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name=_('Measurement unit'),
        help_text=_("Units in which material is entered"),
        unique = True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhMatClass definition', 'Material class')
        verbose_name_plural = tr.pgettext_lazy('AhMatClass definition', 'Material classes')

    def act_display_name(self):
        lang = tr.get_language()
        return self.translated('display_name', default=None, language=lang, fallback=True)

    def act_mat_class_description(self):
        lang = tr.get_language()
        return self.translated('mat_class_description', default=None, language=lang, fallback=True)

    def __str__(self):
        return '{} ({})'.format(self.act_display_name(), self.measurement_unit)


class AhMatClassTranslation(get_translation_model(AhMatClass, "ahmatclass")):
    display_name = models.CharField(
        max_length=200,
        verbose_name=_('Material class display name'),
        help_text=_("Name of the material class for displaying"),
        null=True,
        blank=True,
    )
    mat_class_description =  models.TextField(
        verbose_name=_('Material class description'),
        help_text=_("Text to describe the material class."),
        null=True,
        blank=True,
        unique=False,
    )


#------------------------  AhAnsver
class AhAnswer(models.Model):
    description = models.CharField(
        max_length=200,
        verbose_name=_('Description'),
        help_text=_("Offers description"),
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Owner'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Link to Owner'),
        related_name="owned_answers",
        null=True,
    )
    ah_offer = models.ForeignKey(
        AhOffer,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Offer'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Link to Offer'),
        related_name="answers",
        null=True,
    )
    total_price =  models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Total price'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Final price for the answer'),
        null=True,
        blank=True,
    )
    is_bound = models.BooleanField(
        default=False,
        verbose_name=_('Bound'),
        help_text=_("Mark bound answers. ")
    )
    creator = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Creator'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Link to Creator'),
        related_name="created_answers",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    changed_by = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Last change'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Link to user made last change'),
        null=True, blank=True,
        related_name="last_changed_answers",
    )
    changed_at = models.DateTimeField(auto_now=True,)
    auction_url = models.URLField(
        max_length=200,
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Auction URL'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Online auction url'),
        null=True,
        blank=True,
    )
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_answers',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhAnswer definition', 'Answer')
        verbose_name_plural = tr.pgettext_lazy('AhAnswer definition', 'Answers')

    # def get_absolute_url(self):
    #    return reverse('ah-offer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} ({}) to {} {} ({})'.format(self.pk,
            self.owner.customer_name,
            self.description,
            self.ah_offer.pk,
            self.ah_offer.owner.customer_name,
            self.ah_offer.description
        )

    def get_absolute_url(self):
        return reverse('ah-answer-detail', kwargs={'pk': self.pk})

    @property
    def actual_state(self):
        steps = self.my_steps.all().order_by("-created_at")
        if steps.count() > 0:
            return steps.first().state
        return None

    def is_equal_state(self, state):
        return (self.actual_state == state)

    def get_steps(self):
        return self.my_steps.all().order_by("-created_at")

    def refresh_total_price(self):
        total = 0
        for line in self.my_lines.all():
             total = total + line.total_price
        self.total_price = total
        self.save()


class AhAnswerLine(models.Model):
    ppu =  models.DecimalField(
        max_digits = 7,
        decimal_places = 2,
        default=0.0,
        verbose_name=tr.pgettext_lazy('AhAnswerLine definition', 'Price per unit'),
        help_text=tr.pgettext_lazy('AhAnswerLine definition','Price for one measurement unit'),
    )
    total_price =  models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default=0.0,
        verbose_name=tr.pgettext_lazy('AhAnswerLine definition', 'Total price'),
        help_text=tr.pgettext_lazy('AhAnswerLine definition','Final price for the line'),
    )
    answer = models.ForeignKey(
        AhAnswer,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhAnswerLine definition', 'Answer'),
        help_text=tr.pgettext_lazy('AhAnswerLine definition','Link to Answer'),
        related_name="my_lines",
        null=True,
    )
    offer_line = models.ForeignKey(
        AhOfferLine,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhAnswerLine definition', 'Offer line'),
        help_text=tr.pgettext_lazy('AhAnswerLine definition','Link to line of offer'),
        related_name="answer_lines",
        null=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhAnswerLine definition', 'Answer line')
        verbose_name_plural = tr.pgettext_lazy('AhAnswerLine definition', 'Answer lines')

    # def get_absolute_url(self):
    #    return reverse('ah-offer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} ({}) from {} {}'.format(self.pk,
            self.offer_line.description,
            self.total_price,
            self.answer.id,
            self.answer.description,
        )
