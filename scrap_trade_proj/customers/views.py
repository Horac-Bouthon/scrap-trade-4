from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy, reverse
from .forms import (
    UserRestCreationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CustomerEmailUpdateForm,
    CustomerWebUpdateForm,
    CustomerPhoneUpdateForm,
    CustomerBankUpdateForm,
    CustomerEstUpdateForm,
    CustomerUserUpdateForm,
    CustomerTranUpdateForm,
    PasswordReset,
    PasswordResetRequest,
)
from .models import (
    Customer,
    CustomerEmail,
    CustomerWeb,
    CustomerPhone,
    BasicPhoneCategory,
    CustomerBankAccount,
    CustomerEstablishments,
    CustomerTranslation,
    BasicPhoneCategoryTranslation,
    ProjectCustomUser,
    PasswordResetLink,
)

from project_main.models import Project
from customers.modules.customer_mod import InlineEdit
from integ.models import (
    OpenId,
)

from django.utils import translation as tr
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils.translation import gettext as _

from .permissions import (
    test_user_belong_customer, UserBelongCustomer, user_belong_customer,
    test_can_edit_customer, CanEditCustomer, can_edit_customer,
    test_poweruser, Poweruser, poweruser,
)


class CustomerList(LoginRequiredMixin, ListView):
    model = Customer
    ordering = ['customer_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_header'] = {
            'title': _('Customer list'),
            'desc': _('A list of all signed up customers using the website.'),
        }
        if test_poweruser(self.request.user):
            context['content_header']['button_list'] = [{
                'text': _("Add New Customer"),
                'href': reverse('project-customer-new'),
                'icon': 'plus',
                'type': 'poweruser',
            }]
        return context


class CustomerInfo(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        oid = str(customer.open_id.int_id)
        context['content_header'] = {
            'title': customer.customer_name,
            'desc': _('Detailed customer information'),
            'image': { 'src': customer.customer_logo.url,
                       'alt': _('Customer logo') },
        }
        if test_can_edit_customer(self.request.user, customer):
            context['content_header']['button_list'] = [{
                'text': _("Edit Customer"),
                'href': reverse('project-customer-detail',
                                kwargs={'pk': customer.pk}),
                'icon': 'edit-3',
            }]

        return context


class CustomerDetailView(CanEditCustomer, DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['content_header'] = {
            'title': customer.customer_name + ' | ' + _('Edit'),
            'desc': _("Edit customer details"),
            'image': { 'src': customer.customer_logo.url,
                       'alt': _('Customer logo') },
        }

        button_list = []
        if test_poweruser(self.request.user):
            button_list.append({
                'text': _("Delete Customer"),
                'href': reverse('project-customer-delete',
                                kwargs={'pk': customer.pk}),
                'icon': 'trash-2', 'type': 'danger',
            })
        if customer.open_id:
            oid = str(customer.open_id.int_id)
            button_list.append({
                'text': _("Documents"),
                'href': reverse('doc-repo-dokument-list',
                                kwargs={'oid': oid}),
                'icon': 'eye',
            })
        context['content_header']['button_list'] = button_list

        context['inlines'] = [
            InlineEdit(
                heading = _("E-mails:"),
                owner = customer,
                set = customer.customeremail_set.all,
                form = CustomerEmailUpdateForm,
                create = 'project-customer-email-create',
                delete = 'project-email-delete',
                update = 'project-customer-email-update',
            ),
            InlineEdit(
                heading = _('Websites:'),
                owner = customer,
                set = customer.customerweb_set.all,
                form = CustomerWebUpdateForm,
                create = 'project-customer-web-create',
                delete = 'project-web-delete',
                update = 'project-customer-web-update',
            ),
            InlineEdit(
                heading = _('Establishments:'),
                owner = customer,
                set = customer.customerestablishments_set.all,
                form = CustomerEstUpdateForm,
                create = 'project-customer-est-create',
                delete = 'project-est-delete',
                update = 'project-customer-est-update',
                documents = 'doc-repo-dokument-list',

                view_through_template = 'customers/__address.html',
            ),
            InlineEdit(
                heading = _('Phones:'),
                owner = customer,
                set = customer.customerphone_set.all,
                form = CustomerPhoneUpdateForm,
                create = 'project-customer-phone-create',
                delete = 'project-phone-delete',
                update = 'project-customer-phone-update',

                view_through_template = 'customers/__phone.html',
            ),
            InlineEdit(
                heading = _('Bank accounts:'),
                owner = customer,
                set = customer.customerbankaccount_set.all,
                form = CustomerBankUpdateForm,
                create = 'project-customer-bank-create',
                delete = 'project-bank-delete',
                update = 'project-customer-bank-update',

                view_through_template = 'customers/__bank.html',
            ),
        ]

        return context



class CustomerCreateView(Poweruser, CreateView):
    model = Customer
    fields = ['customer_name','customer_ICO','customer_DIC',
              'customer_background','customer_logo']
    template_name = "customers/customer_create.html"


class CustomerUpdateView(CanEditCustomer, UpdateView):
    model = Customer
    fields = ['customer_name','customer_ICO','customer_DIC',
              'customer_background','customer_logo']


class CustomerDeletelView(Poweruser, DeleteView):
    model = Customer
    success_url = reverse_lazy('project-customer-home')



# http://127.0.0.1:8079/customers/2/email/2
# ------------------------- CustomerEmail
@can_edit_customer
def customer_email_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    email = CustomerEmail.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerEmailUpdateForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            success_message = _('Your e-mail has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerEmailUpdateForm(instance=email)

    title2 = tr.pgettext('customer_email_update-title', 'update-email')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/email_form.html', context)


@can_edit_customer
def customer_email_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = CustomerEmailUpdateForm(request.POST)
        if form.is_valid():
            customer.customeremail_set.create(
                customer_email = form.cleaned_data['customer_email'],
                customer = customer,
            )
            success_message = _('Your e-mail has been added!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerEmailUpdateForm()

    title2 = tr.pgettext('customer_email_update-title', 'create-email')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/email_form.html', context)


class CustomerDeletelEmail(CanEditCustomer, DeleteView):
    model = CustomerEmail

    # @todo; Why do we have two different redirect methods in delete views? Also, they're the same everywhere so we could probably inherit that functionality.

    def delete(self, *args, **kwargs):
        self.customer_pk = self.get_object().customer.id
        super().delete(*args, **kwargs)
        return redirect('project-customer-detail',
                        self.object.customer.pk)

    def get_success_url(self):
        return reverse_lazy('project-customer-detail',
                            kwargs={'pk': self.customer_pk})


# ------------------------- CustomerWeb
@can_edit_customer
def customer_web_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = CustomerWebUpdateForm(request.POST)
        if form.is_valid():
            customer.customerweb_set.create(
                customer_web = form.cleaned_data['customer_web'],
                customer = customer,
            )
            success_message = _('Your web url has been added!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerWebUpdateForm()

    title2 = tr.pgettext('customer_web_update-title', 'create-phone')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerweb_form.html', context)

@can_edit_customer
def customer_web_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    web = CustomerWeb.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerWebUpdateForm(request.POST, instance=web)
        if form.is_valid():
            form.save()
            success_message = _('Your web url has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerWebUpdateForm(instance=web)

    title2 = tr.pgettext('customer_web_update-title', 'update-web')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerweb_form.html', context)


class CustomerDeletelWeb(CanEditCustomer, DeleteView):
    model = CustomerWeb

    def delete(self, *args, **kwargs):
        self.customer_pk = self.get_object().customer.id
        super().delete(*args, **kwargs)
        return redirect('project-customer-detail',
                        self.object.customer.pk)

    def get_success_url(self):
        return reverse_lazy('project-customer-detail',
                            kwargs={'pk': self.customer_pk})


# ------------------------- CustomerPhone
@can_edit_customer
def customer_phone_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = CustomerPhoneUpdateForm(request.POST)
        if form.is_valid():
            customer.customerphone_set.create(
                customer_phone = form.cleaned_data['customer_phone'],
                desctiption = form.cleaned_data['desctiption'],
                category = form.cleaned_data['category'],
                customer = customer,
            )
            success_message = _('Your phone has been added!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerPhoneUpdateForm()

    title2 = tr.pgettext('customer_web_update-title', 'create-phone')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerphone_form.html', context)


@can_edit_customer
def customer_phone_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    phone = CustomerPhone.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerPhoneUpdateForm(request.POST, instance=phone)
        if form.is_valid():
            form.save()
            success_message = _('Your phone has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerPhoneUpdateForm(instance=phone)

    title2 = tr.pgettext('customer_phone_update-title', 'update-phone')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerphone_form.html', context)


class CustomerDeletelPhone(CanEditCustomer, DeleteView):
    model = CustomerPhone

    def delete(self, *args, **kwargs):
        self.customer_pk = self.get_object().customer.id
        super().delete(*args, **kwargs)
        return redirect('project-customer-detail', self.object.customer.pk)

    def get_success_url(self):
        return reverse_lazy('project-customer-detail',  kwargs={'pk': self.customer_pk})

# ---------------------------------------------------- CustomerBankAccount
@can_edit_customer
def customer_bank_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = CustomerBankUpdateForm(request.POST)
        if form.is_valid():
            customer.customerbankaccount_set.create(
                account = form.cleaned_data['account'],
                bank_id = form.cleaned_data['bank_id'],
                iban = form.cleaned_data['iban'],
                customer = customer,
            )
            success_message = _('Your phone has been added!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerBankUpdateForm()

    title2 = tr.pgettext('customer_bank_create-title', 'create-bank-account')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerbankaccount_form.html', context)


@can_edit_customer
def customer_bank_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    bank = CustomerBankAccount.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerBankUpdateForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            success_message = _('Your bank account has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerBankUpdateForm(instance=bank)

    title2 = tr.pgettext('customer_bank_update-title', 'update-bank')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerbankaccount_form.html', context)


class CustomerDeletelBank(CanEditCustomer, DeleteView):
    model = CustomerBankAccount

    def delete(self, *args, **kwargs):
        self.customer_pk = self.get_object().customer.id
        super().delete(*args, **kwargs)
        return redirect('project-customer-detail', self.object.customer.pk)

    def get_success_url(self):
        return reverse_lazy('project-customer-detail',  kwargs={'pk': self.customer_pk})


# ----------------------------------------------------  CustomerEstablishments
@can_edit_customer
def customer_est_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = CustomerEstUpdateForm(request.POST)
        if form.is_valid():
            customer.customerestablishments_set.create(
                establishment = form.cleaned_data['establishment'],
                address_street = form.cleaned_data['address_street'],
                address_number = form.cleaned_data['address_number'],
                address_town = form.cleaned_data['address_town'],
                address_zip_code = form.cleaned_data['address_zip_code'],
                is_headquarter = form.cleaned_data['is_headquarter'],
                customer = customer,
            )
            success_message = _('Your establishment has been added!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerEstUpdateForm()

    title2 = tr.pgettext('customer_est_create-title', 'create-establishment')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerestablishments_form.html', context)


@can_edit_customer
def customer_est_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    est = CustomerEstablishments.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerEstUpdateForm(request.POST, instance=est)
        if form.is_valid():
            form.save()
            success_message = _('Your establishment has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerEstUpdateForm(instance=est)

    title2 = tr.pgettext('customer_bank_update-title', 'update-establishment')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/customerestablishments_form.html', context)


class CustomerDeletelEst(CanEditCustomer, DeleteView):
    model = CustomerEstablishments

    def delete(self, *args, **kwargs):
        self.customer_pk = self.get_object().customer.id
        super().delete(*args, **kwargs)
        return redirect('project-customer-detail', self.object.customer.pk)

    def get_success_url(self):
        return reverse_lazy('project-customer-detail',  kwargs={'pk': self.customer_pk})


# http://127.0.0.1:8079/customers/2/user/new
# ---------------------------------------------------- ProjectCustomUser

@can_edit_customer
def customer_user_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':

        form = UserRestCreationForm(request.POST)
        if form.is_valid():
            new_user = customer.projectcustomuser_set.create(
                email = form.cleaned_data['email'],
                name = form.cleaned_data['name'],
                customer = customer,
            )
            for group in form.cleaned_data['groups']:
                new_user.groups.add(group)

            # Setting the user's password...
            new_user.set_unusable_password()
            # Send the user into the DB.
            new_user.save()
            password_link = PasswordResetLink(
                for_user = new_user
            )
            password_link.save()
            password_link.send_to_user(request)

            msg = _("The user has been created. ") + ' ' +\
            _("An email with a link for setting a new password has been sent to the user's address.") + ' ' +\
            _("This link is valid for 48 hours from now.")
            # @todo; For user create message, use variables in the translation with user's name, email address and a variable for the actual expiry time
            messages.success(request, msg)
            return redirect('project-customer-detail', pk)
    else:
        form = UserRestCreationForm()

    title2 = tr.pgettext('customer_user_create-title', 'create-user')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'customers/projectcustomuser_form.html', context)



def request_password_reset_link(request):
    """
    View used for asking for a password reset link with entering
    the username. GET presents the form, POST invokes sending
    the email, if it corresponds to ~some~ user in the system.
    """

    if request.method == 'GET':
        empty_form = PasswordResetRequest()
        return render(request, 'customers/reset_password.html', {
            'request_form': empty_form
        })

    elif request.method == 'POST':

        filled_form = PasswordResetRequest(request.POST)
        if filled_form.is_valid():
            email = filled_form.cleaned_data['email']
            try:
                user = ProjectCustomUser.objects.get(email=email)
            except Exception:
                # Do nothing. We don't want hackers to know that the user
                # doesn't exist.
                pass

            # Register the link, make the link's id
            new_link = PasswordResetLink(for_user=user)
            new_link.save()
            new_link.send_to_user(request)

        # Return the same success message regardless of whether the user
        # is valid or not. This is a security measure to not allow
        # bots to know if the user exists or not by spamming this page.
        msg = _("A reset link has been sent to the email address. ") + ' ' +\
        _("If you didn't recieve any email, make sure that your address has been typed correctly ") + ' ' +\
        _(" and that the message wasn't marked as spam. ")
        messages.success(request, msg)
        return redirect('user-login')


def reset_password(request, uuid):
    """
    Target of the reset password link. This is what you'll get
    when clicking on the reset link. GET presents the form to
    enter the new password, POST validates the form and changes
    the user's password.
    """

    # Always validate the link
    pass_reset_link = None
    try:
        pass_reset_link = PasswordResetLink.objects.get(id=uuid)
        print('pass_reset_link = {}'.format(pass_reset_link))
        if pass_reset_link.is_not_valid_anymore():
            pass_reset_link = None
    except Exception:
        pass_reset_link = None

    if pass_reset_link == None:
        msg = _("The password reset link is either invalid or expired.")
        messages.warning(request, msg)
        return redirect('user-login')


    if request.method == 'GET' and pass_reset_link:
        # Construct a form for changing the password (2 passwords)
        return render(request, 'customers/reset_password.html', {
            'password_form': PasswordReset(),
            'for_user': pass_reset_link.for_user,
        })

    elif request.method == 'POST':
        filled_form = PasswordReset(request.POST)

        if filled_form.is_valid() and pass_reset_link:
            # Re-set the password
            pass_reset_link.reset_password(
                filled_form.cleaned_data['new_password']
            )
            #------------ CLEAN models
            pass_reset_link.delete()
            msg = _("You have successfully changed your password. ") + ' ' +\
            _("You can now use the new password to log into your account.")
            messages.success(request, msg)
            return redirect('user-login')

        else:
            # Reload; error messages are added to the filled form
            # by the form validation itself.
            return render(request, 'customers/reset_password.html', {
                'password_form': filled_form
            })




# http://127.0.0.1:8079/customers/2/user/9
@can_edit_customer
def customer_user_update(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    user = ProjectCustomUser.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = CustomerUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            success_message = _('User has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-detail', pk)
    else:
        form = CustomerUserUpdateForm(instance=user)

    title2 = tr.pgettext('customer_user_update-title', 'update-user')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
        'user_name': user.name,
        'user_email': user.email,
    }
    return render(request, 'customers/projectcustomuser_active.html', context)


# ----------------------------------------------------  CustomerTranslation
@can_edit_customer
def customer_tran_update(request, pk, lang):
    customer = Customer.objects.filter(id = pk).first()
    set_lang = lang
    try:
        tran = customer.get_translation(lang, fallback=False)
    except:
        tran = customer.translations.create(
            customer_description = "",
            short_description = "",
            model = customer,
            language = lang,
        )
    if not tran:
        tran = customer.translations.create(
            customer_description = "",
            short_description = "",
            model = customer,
            language = lang,
        )

    if request.method == 'POST':
        form = CustomerTranUpdateForm(request.POST, instance=tran)
        defa = 'not set'
        change_lan = request.POST.get('language-switch', defa)
        print("change_lan = {}".format(change_lan))
        if change_lan not in 'not set':
            return redirect('project-customer-tran', pk, change_lan)
        if form.is_valid():
            form.save()
            success_message = _('Your translation has been updated!')
            messages.success(request, success_message)
            return redirect('project-customer-update', pk)
    else:
        form = CustomerTranUpdateForm(instance=tran)

    title2 = tr.pgettext('customer_tran_update-title', 'update-translation')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
        'set_lang': set_lang,
    }
    return render(request, 'customers/customer_translation.html', context)


# ----------------------------------------------------


def log_in(request):
    
    if request.method == 'GET':
        form = AuthenticationForm()
    
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user_f = form.get_user()
            login(request, user_f)
            messages.success(request, _('Successfully logged in'))
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
        
    context = {
        'form': form,
        'title': tr.pgettext('customer-login-title', 'Login'),
    }
    return render(request, 'customers/login.html', context)

def log_out(request):
    logout(request)
    messages.success(request, _('You have been logged out'))
    return redirect('user-login')



@login_required
def profile(request):
    proj = Project.objects.all().first()
    oid = str(request.user.userprofile.open_id.int_id)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            success_message = _('Your account has been updated!')
            messages.success(request, success_message)
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    title2 = tr.pgettext('customer-user-profile-title', 'user-profile')
    context = {
        'u_form': user_form,
        'p_form': profile_form,
        'title': title2,
        'project': proj,
        'oid': oid,
    }
    return render(request, 'customers/user_profile.html', context)
