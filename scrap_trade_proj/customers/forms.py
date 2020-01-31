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


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectCustomUser
        fields = ['name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['language', 'image']


class CustomerDescriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name','customer_ICO','customer_DIC','customer_background','customer_logo']


class CustomerEmailUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerEmail
        fields = ['customer_email','is_private_adr','is_admin_adr','is_business_adr','language']


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
