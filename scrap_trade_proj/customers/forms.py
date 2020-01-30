from django import forms
from .models import (
    ProjectCustomUser,
    UserProfile,
    Customer,
    CustomerEmail,
    CustomerWeb,
    CustomerPhone,
    CustomerBankAccount,
    CustomerEstablishments,
    ProjectCustomUser,
    CustomerTranslation,
)


from django.utils.translation import gettext as _


class UserRestCreationForm(forms.ModelForm):
    """
    A form for creating new users.
    """

    class Meta:
        model = ProjectCustomUser
        fields = ('email', 'name', 'groups')  # @todo; Make a better Groups option list -> list of checkboxes with labels (frontend-only task)

    def clean_password_repeated(self):
        # Check that the two password entries match
        pw = self.cleaned_data.get("password")
        pw_rep = self.cleaned_data.get("password_repeated")
        if (pw and pw_rep) and (pw != pw_rep):
            raise forms.ValidationError(
                _("Passwords don't match")
            )
        return pw_rep

    def __init__(self, *args, **kwargs):
        super(UserRestCreationForm, self).__init__(*args, **kwargs)
        qs = Group.objects.filter(name = 'customer_admin') | Group.objects.filter(name = 'customer_worker')
        self.fields['groups'].queryset = qs.order_by("name")


class PasswordResetRequest(forms.Form):
    email = forms.EmailField(
        help_text=_(("Enter the email address used for logging in to "
                     "your account. ")),
    )
    

class PasswordReset(forms.Form):
    
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_("Enter a new password for yor account.")
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_("Repeat the same password.")
    )
    
    def clean(self, *args, **kwargs):
        # Validate 'required'-ness
        super().clean()
        # Validate if passwords match
        data = self.cleaned_data
        if data['new_password'] != data['password_confirmation']:
            raise forms.ValidationError(
                _("The passwords don't match. Please try writing them again."),
            )
        # @todo; Add the builtin django security criteria (length, special characters, similiarity to the username...)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectCustomUser
        fields = ['name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class CustomerDescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name','customer_ICO','customer_DIC','customer_background','customer_logo']


class CustomerEmailUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerEmail
        fields = ['customer_email']


class CustomerWebUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerWeb
        fields = ['customer_web']


class CustomerPhoneUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerPhone
        fields = ['customer_phone', 'desctiption', 'category']


class CustomerBankUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerBankAccount
        fields = ['account', 'bank_id', 'iban']


class CustomerEstUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerEstablishments
        fields = ['establishment', 'address_street', 'address_number', 'address_town', 'address_zip_code', 'is_headquarter']


class CustomerUserUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectCustomUser
        fields = ['is_active']

class CustomerTranUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerTranslation
        fields = ['short_description', 'customer_description']
