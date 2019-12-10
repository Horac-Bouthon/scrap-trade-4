from django.db import models
from datetime import datetime
from django import forms
from customers.models import (
    Customer,
    ProjectCustomUser,
)
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
    is_new = models.BooleanField(
        default=True,
        verbose_name=_('New'),
        help_text=_("New created offer. ")
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name=_('Confirmed'),
        help_text=_("Offers is confirmed by owner. ")
    )
    confirmed_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Confirmed at'),
        null=True,
        blank=True,
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_('Accepted'),
        help_text=_("Mark offers accepted by the buyer.")
    )
    accepted_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Accepted at'),
        null=True,
        blank=True,
    )
    is_ready_close = models.BooleanField(
        default=False,
        verbose_name=_('Ready to close'),
        help_text=_("Mark ready to close offers.")
    )
    ready_close_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Ready to close at'),
        null=True,
        blank=True,
    )
    is_closed = models.BooleanField(
        default=False,
        verbose_name=_('Closed'),
        help_text=_("Mark closed offers. ")
    )
    closed_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Closed at'),
        null=True,
        blank=True,
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name=_('Cancelled'),
        help_text=_("Mark cancelled offers. ")
    )
    canceled_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Canceled at'),
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
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Delivery date'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of the delivery'),
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
        help_text=tr.pgettext_lazy('AhOffer definition','List of customers who received the offer'),
        related_name="receive_offers",
        blank=True,
    )
    delivery_date = models.DateField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Delivery date'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of the delivery'),
        null=True,
        blank=True,
    )
    auction_date = models.DateField(
        verbose_name=tr.pgettext_lazy('AhOffer definition', 'Auction date'),
        help_text=tr.pgettext_lazy('AhOffer definition','Date of auction'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('AhOffer definition', 'Offer')
        verbose_name_plural = tr.pgettext_lazy('AhOffer definition', 'Offers')

    def get_absolute_url(self):
        return reverse('ah-offer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} ({}) {}'.format(self.pk, self.owner.customer_name, self.description, self.created_at)


#------------------------  AhOfferLine
class AhOfferLine(models.Model):
    description = models.CharField(
        max_length=200,
        verbose_name=_('Description'),
        help_text=_("Offers line description"),
        null=True,
        blank=True,
    )
    amount =  models.DecimalField(
        max_digits = 10,
        decimal_places = 4,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Amount'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Quantity of material'),
        null=True,
        blank=True,
    )
    offer = models.ForeignKey(
        'AhOffer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Offer'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Link to Offer'),
        related_name="lines",
        null=True,
        blank=True,
    )
    mat_class = models.ForeignKey(
        'AhMatClass',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('AhOfferLine definition', 'Material class'),
        help_text=tr.pgettext_lazy('AhOfferLine definition','Link to Material class'),
        related_name="used_lines",
        null=True,
        blank=True,
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
    is_new = models.BooleanField(
        default=True,
        verbose_name=_('New'),
        help_text=_("New created offer. ")
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name=_('Confirmed'),
        help_text=_("Answer is confirmed by owner. ")
    )
    confirmed_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Confirmed at'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Confirmed from...'),
        null=True,
        blank=True,
    )
    is_successful = models.BooleanField(
        default=False,
        verbose_name=_('Successful'),
        help_text=_("Mark successful answers. ")
    )
    is_bound = models.BooleanField(
        default=False,
        verbose_name=_('Bound'),
        help_text=_("Mark bound answers. ")
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_('Accepted'),
        help_text=_("Mark accepted answers. ")
    )
    accepted_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Accepted at'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Accepted from...'),
        null=True,
        blank=True,
    )
    is_closed = models.BooleanField(
        default=False,
        verbose_name=_('Closed'),
        help_text=_("Mark closed answers. ")
    )
    closed_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Closed at'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Closed from...'),
        null=True,
        blank=True,
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name=_('Cancelled'),
        help_text=_("Mark cancelled answers. ")
    )
    canceled_at = models.DateTimeField(
        verbose_name=tr.pgettext_lazy('AhAnswer definition', 'Canceled at'),
        help_text=tr.pgettext_lazy('AhAnswer definition','Canceled from...'),
        null=True,
        blank=True,
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
