from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.urls import reverse
from PIL import Image
import os

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from translatable.models import TranslatableModel, get_translation_model

from project_main.models import Project

# Create your models here.
class ProjectCustomUserManager(BaseUserManager):
    """Helps Django work with custom user model """

    def create_user(self, name, email, password=None, customer=None):
        """ Create new custom user object """
        if not email:
            raise ValueError(_('User must have an email address.'))
        email = self.normalize_email(email)
        proj = Project.objects.all().first()
        print('project>')
        print(proj)
        if customer is not None:
            user = self.model(email=email, name=name, customer=customer, project=proj)
        else:
            user = self.model(email=email, name=name, project=proj)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        """ Create and saves new super custom user object """
        user = self.create_user(name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ProjectCustomUser(AbstractBaseUser, PermissionsMixin):
    """ basic user for admin AND customer base users """
    email = models.EmailField(max_length=255, verbose_name=_('email address'), unique=True,
                    help_text=_("Required: 150 characters or fewer. Letters, digits and @/./+/-/_ only."))
    name = models.CharField(max_length=255, verbose_name=_('user name'), help_text=_("User identification"))
    is_active = models.BooleanField(default=True, verbose_name=_('active user'), help_text=_("User can log in"))
    is_staff = models.BooleanField(default=False, verbose_name=_('access admin tools'),
                    help_text=_("User can access administration tools"))
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('ProjectCustomUser definition', 'Customer'),
        help_text=tr.pgettext_lazy('ProjectCustomUser definition','Link to Customer'),
        null=True, blank=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('ProjectCustomUser definition', 'Project'),
        help_text=tr.pgettext_lazy('ProjectCustomUser definition','Link to Project'),
        null=True, blank=True,
    )

    objects = ProjectCustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = tr.pgettext_lazy('ProjectCustomUser definition', 'User')
        verbose_name_plural = tr.pgettext_lazy('ProjectCustomUser definition', 'Users')
        permissions = (
            ('is_poweruser', 'custom -- poweruser'),
            ('is_customer_admin', 'custom -- customer-admin'),
            ('is_customer_user', 'custom -- customer-user'),
        )

    def get_full_name(self):
        """ Used to get users full name """
        return self.name

    def get_short_name(self):
        """ Used to get users short name """
        return self.name

    def __str__(self):
        """ Used to get object in string presentation """
        return self.email


class UserProfile(models.Model):
    """ Additiona information for user """
    user = models.OneToOneField(ProjectCustomUser, on_delete=models.CASCADE,
                    verbose_name=tr.pgettext_lazy('UserProfile user', 'user'))
    image = models.ImageField(default="default-user.jpg", upload_to='profile_pics',
                        verbose_name=tr.pgettext_lazy('UserProfile image', 'image'))

    class Meta:
        verbose_name = tr.pgettext_lazy('UserProfile definition', 'User Profile')
        verbose_name_plural = tr.pgettext_lazy('UserProfile definition', 'User Profiles')

    def __str__(self):
        return '{} profile'.format(self.user.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CustomerEstablishments(models.Model):
    establishment = models.CharField(max_length=100, verbose_name=_('Establishment'),
            help_text=_("Establishment name"))
    address_street = models.CharField(max_length=255, verbose_name=_('Street'),
            help_text=_("Street in address"))
    address_number =   models.CharField(max_length=255, verbose_name=_('House'),
            help_text=_("House number in address"))
    address_town =   models.CharField(max_length=255, verbose_name=_('City'),
            help_text=_("City name in address"))
    address_zip_code =   models.CharField(max_length=255, verbose_name=_('ZIP'),
            help_text=_("ZIP code in address"))
    is_headquarter = models.BooleanField(default=False, verbose_name=_('headquarter'),
                    help_text=_("Mark customers headquarter. "))
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerEstablishments definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerEstablishments definition','Link to Customer'),
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerEstablishments definition', 'Establishment')
        verbose_name_plural = tr.pgettext_lazy('CustomerEstablishments definition', 'Establishments')

    def __str__(self):
        var_address = tr.pgettext_lazy('CustomerAddress __str__', 'establishment')
        return '{} {} {} {}'.format(var_address, self.establishment, self.address_street, self.address_town)


class CustomerEmail(models.Model):
    customer_email = models.EmailField(max_length=255, verbose_name=tr.pgettext_lazy('Customer definition', 'email address'),
                    help_text=tr.pgettext_lazy('Customer definition', "Required: 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
                    null=True, blank=True,)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerEmail definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerEmail definition','Link to Customer'),
        null=True, blank=True,
    )
    is_admin_adr = models.BooleanField(default=False, verbose_name=_('admin address'),
                    help_text=_("Mark special addresses to send additional administration messages. "))

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerEmail definition', 'Customer email')
        verbose_name_plural = tr.pgettext_lazy('CustomerEmail definition', 'Customer emails')

    def __str__(self):
        var_address = _('address')
        return self.customer_email

class CustomerBankAccount(models.Model):
    account = models.CharField(max_length=50, verbose_name=_('Account number'),
            help_text=_("Account number"))
    bank_id = models.CharField(max_length=4, verbose_name=_('Bank ID'),
            help_text=_("National identification of the bank"))
    iban = models.CharField(max_length=100, verbose_name=_('IBAN'),
            help_text=_("International account identification"))
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerEmail definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerEmail definition','Link to Customer'),
        null=True, blank=True,
    )
    is_prefered = models.BooleanField(default=False, verbose_name=_('Prefered account'),
                    help_text=_("Preferably use this account."))

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerBankAccount definition', 'Customer bank account')
        verbose_name_plural = tr.pgettext_lazy('CustomerBankAccount definition', 'Customer bank accounts')

    def __str__(self):
        return "{}/{} ({})".format(self.account, self.bank_id, self.iban)

class BasicPhoneCategory(TranslatableModel):
    phone_type = models.CharField(
        max_length=50,
        default="phone",
        verbose_name=tr.pgettext_lazy('BasicPhoneCategory definition', 'Type'),
        help_text=tr.pgettext_lazy('BasicPhoneCategory definition','Phone category type'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('BasicPhoneCategory definition', 'Phone category')
        verbose_name_plural = tr.pgettext_lazy('BasicPhoneCategory definition', 'Phone categories')

    def __str__(self):
        return self.phone_type

    def act_category_name(self):
        lang = tr.get_language()
        return self.translated('category', default=None, language=lang, fallback=True)

class BasicPhoneCategoryTranslation(get_translation_model(BasicPhoneCategory, "basicphonecategory")):
    category = models.CharField("category", max_length=50, unique=False)


class CustomerPhone(models.Model):
    customer_phone = models.CharField(max_length=255, verbose_name=_('Customer phone'),
        help_text=_("Customer phone number"))
    desctiption = models.CharField(max_length=255, verbose_name=_('Description'),
        help_text=_("Phone description"), null=True, blank=True,)

    category = models.ForeignKey(
        'BasicPhoneCategory',
        default=1,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerPhone definition', 'Phone category'),
        help_text=tr.pgettext_lazy('CustomerPhone definition','Category of the phone'),
    )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerPhone definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerPhone definition','Link to Customer'),
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerEmail definition', 'Customer phone')
        verbose_name_plural = tr.pgettext_lazy('CustomerEmail definition', 'Customer phones')

    def __str__(self):
        return self.customer_phone



class CustomerWeb(models.Model):
    customer_web = models.URLField(max_length=200, verbose_name=_('Customer web'),
                    help_text=_('Customers website URL'),
                    null=True, blank=True,)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerEmail definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerEmail definition','Link to Customer'),
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerWeb definition', 'Customer website')
        verbose_name_plural = tr.pgettext_lazy('CustomerWeb definition', 'Customer websites')

    def __str__(self):
        var_address = _('address')
        return self.customer_web

class Customer(TranslatableModel):
    customer_name =  models.CharField(
        max_length=255, verbose_name=_('Customer name'),
        help_text=_("Customer identification")
    )
    customer_ICO =  models.CharField(
        max_length=50, verbose_name=_('Registration number'),
        help_text=_("Customer registration number"),
        null=True, blank=True,
    )
    customer_DIC =  models.CharField(
        max_length=50, verbose_name=_('VAT'),
        help_text=_("Customer VAT number"),
        null=True, blank=True,
    )
    customer_background = models.ImageField(
        default="default-background.jpg",
        upload_to='profile_pics',
        verbose_name=tr.pgettext_lazy('Customer image', 'Background'),
        help_text=_('Image to fill customers web page background')
    )
    customer_logo = models.ImageField(
        default="default-logo.jpg",
        upload_to='profile_pics',
        verbose_name=tr.pgettext_lazy('Customer image', 'Logo'),
        help_text=_('Customer logo')
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('Customer definition', 'Customer')
        verbose_name_plural = tr.pgettext_lazy('Customer definition', 'Customers')

    def __str__(self):
        var_address = _('address')
        return self.customer_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.customer_logo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.customer_logo.path)

    def get_absolute_url(self):
        return reverse('project-customer-detail', kwargs={'pk': self.pk})

    def act_description(self):
        lang = tr.get_language()
        return self.translated('customer_description', default=None, language=lang, fallback=True)

    def act_short(self):
        lang = tr.get_language()
        return self.translated('short_description', default=None, language=lang, fallback=True)


class CustomerTranslation(get_translation_model(Customer, "customer")):
    customer_description =  models.TextField(
        verbose_name=_('Customer description'),
        help_text=_("Text to describe the Customer extensively."),
        null=True,
        blank=True,
        unique=False,
    )
    short_description =  models.TextField(
        verbose_name=_('Short description'),
        help_text=_("Short text to describe the Customer."),
        null=True,
        blank=True,
        unique=False,
    )
