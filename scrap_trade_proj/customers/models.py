from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import Group
from PIL import Image

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from translatable.models import TranslatableModel, get_translation_model

from project_main.models import Project
from integ.models import OpenId
from notification.modules import ntf_manager

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = ProjectCustomUserManager()

    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name=_('email address'),
        help_text=_("This acts as the username when logging in.")
        # @todo; Add an explanation that this email will recieve a one-time link to the password reset page.
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_("Only informational.")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'),
        help_text=_("User can log into the website and isn't blocked.")
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('access admin tools'),
        help_text=_("User can access administration tools")
    )

    customer = models.ForeignKey(
        'Customer',
        null=True,
        blank=True,
        on_delete=models.CASCADE,

        verbose_name=tr.pgettext_lazy(
            'ProjectCustomUser definition', 'Customer'),
        help_text=tr.pgettext_lazy(
            'ProjectCustomUser definition', 'Link to Customer'),
    )
    project = models.ForeignKey(  # @todo; Causes NoneType errors if removed
        Project,
        null=True, blank=True,
        on_delete=models.SET_NULL,

        verbose_name=tr.pgettext_lazy(
            'ProjectCustomUser definition', 'Project'),
        help_text=tr.pgettext_lazy(
            'ProjectCustomUser definition','Link to Project'),
    )

    class Meta:
        verbose_name = tr.pgettext_lazy(
            'ProjectCustomUser definition', 'User')
        verbose_name_plural = tr.pgettext_lazy(
            'ProjectCustomUser definition', 'Users')
        permissions = (
            ('is_poweruser', 'custom -- poweruser'),
            ('is_customer_admin', 'custom -- customer-admin'),
            ('is_customer_user', 'custom -- customer-user'),
        )

    def __str__(self):
        """ Used to get object in string presentation """
        return self.email


import uuid
import django.utils.timezone as django_timezone  # Always use django timezones
from django.urls import reverse  # For making reset urls

class PasswordResetLink(models.Model):
    """
    A link with an expiration datetime that allows a user
    to reset their password, if they know this object's ID.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    for_user = models.ForeignKey(
        'ProjectCustomUser',
        on_delete=models.CASCADE,  # Delete links if user is deleted
    )
    used = models.DateTimeField(
        blank=True, null=True
    )

    def make_expiry_datetime_from_now():
        # Use this as a static method. Django migrate doesn't like
        # @staticmethod and fails to serialize if present.
        VALID_FOR = django_timezone.timedelta(
            hours=48
        )
        # @todo; Expose `VALID_FOR` of password links to be used for user information
        return django_timezone.now() + VALID_FOR

    valid_until = models.DateTimeField(
        default = make_expiry_datetime_from_now  # Callable func, not value!
    )

    def is_not_valid_anymore(self):
        expired = django_timezone.now() > self.valid_until
        used_already = self.used is not None
        return expired or used_already


    def send_to_user(self, request):
        # Make a URL link out of the id
        url = reverse('user-reset', kwargs={'uuid': self.id})
        full_url = request.build_absolute_uri(url)
        context = ntf_manager.NtfContext()
        context['access_url'] = full_url
        address_obj = (self.for_user.email, self.for_user.userprofile.language)
        ntf_manager.send_by_template_to_address(request, context, address_obj, 'set_password')

    def reset_password(self, new_password):
        user = self.for_user
        user.set_password(new_password)
        user.save()
        # Make the link unusable for repeated password changes
        # and note when somebody changed their password.
        self.used = django_timezone.now()
        self.save()



class UserProfile(models.Model):
    """ Additiona information for user """
    user = models.OneToOneField(
        ProjectCustomUser,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile user', 'user'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to pattern object'),
    )
    language = models.CharField(
        default=settings.LANGUAGE_CODE,
        verbose_name=tr.pgettext_lazy('UserProfile user', "language"),
        help_text=tr.pgettext_lazy('UserProfile definition','Set the language to communicate with the user'),
        max_length=15,
        choices=settings.LANGUAGES,
    )
    image = models.ImageField(
        default="default-user.jpg",
        upload_to='profile_pics',
        verbose_name=tr.pgettext_lazy('UserProfile image', 'image'),
        help_text=tr.pgettext_lazy('UserProfile definition','Here you can add an image to the profile'),
    )
    open_id = models.ForeignKey(
        OpenId,
        related_name='my_user_profs',
        null=True,
        blank=True,
        on_delete=models.CASCADE,

        verbose_name=tr.pgettext_lazy(
            'UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy(
            'UserProfile definition','Link to integration key'),
    )

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
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_estab',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('CustomerEstablishments definition', 'Establishment')
        verbose_name_plural = tr.pgettext_lazy('CustomerEstablishments definition', 'Establishments')

    def __str__(self):
        var_address = tr.pgettext_lazy('CustomerAddress __str__', 'establishment')
        return '{} {} {} {}'.format(var_address, self.establishment, self.address_street, self.address_town)


class CustomerEmail(models.Model):
    customer_email = models.EmailField(
        max_length=255,
        verbose_name=tr.pgettext_lazy('Customer definition', 'email address'),
        help_text=tr.pgettext_lazy('Customer definition', "Required: 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('CustomerEmail definition', 'Customer'),
        help_text=tr.pgettext_lazy('CustomerEmail definition','Link to Customer'),
        null=True, blank=True,
    )
    is_private_adr = models.BooleanField(
        default=False,
        verbose_name=_('Private address'),
        help_text=_("This address will not be included in the info. ")
    )
    is_admin_adr = models.BooleanField(
        default=False,
        verbose_name=_('Admin address'),
        help_text=_("Mark special addresses to send additional administration messages. ")
    )
    is_business_adr = models.BooleanField(
        default=False,
        verbose_name=_('Business address'),
        help_text=_("Business messages will be sent to this address")
    )
    language = models.CharField(
        default=settings.LANGUAGE_CODE,
        verbose_name=tr.pgettext_lazy('UserProfile user', "language"),
        help_text=tr.pgettext_lazy('UserProfile definition','Set the language to communicate with the user'),
        max_length=15,
        choices=settings.LANGUAGES,
    )

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
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_customers',
        null=True, blank=True,
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

    #--- ntf_support
    def add_emails(self, ntf_message, admin=False, business=False):
        for email in self.customeremail_set.all():
            if admin:
                if email.is_admin_adr:
                    ntf_message.reciver_list.append((email.customer_email, email.language))
                    continue
            if business:
                if email.is_business_adr:
                    ntf_message.reciver_list.append((email.customer_email, email.language))
                    continue
            if admin == False and business == False:
                ntf_message.reciver_list.append((email.customer_email, email.language))
        return ntf_message

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
