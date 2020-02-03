from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from customers.models import (ProjectCustomUser,
    UserProfile,
    CustomerEstablishments,
    CustomerEmail,
    CustomerWeb,
    Customer,
    CustomerTranslation,
    CustomerPhone,
    BasicPhoneCategory,
    BasicPhoneCategoryTranslation,
    CustomerBankAccount,
    CustomerTranslation,
    PasswordResetLink,
)

from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput, help_text=_("Enter password"))
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput, help_text=_("Confirm password"))

    class Meta:
        model = ProjectCustomUser
        fields = ('email', 'name', 'groups')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ProjectCustomUser
        fields = ('email', 'password', 'name', 'is_active', 'groups', 'project')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'customer', 'project', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'customer', 'groups', 'project')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class BasicPhoneCategoryTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
    model = BasicPhoneCategoryTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1

class BasicPhoneCategoryAdmin(admin.ModelAdmin):
    inlines = [BasicPhoneCategoryTranslationInlineAdmin,]


class CustomerTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
    model = CustomerTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerTranslationInlineAdmin,]


# Register your models here.
admin.site.register(ProjectCustomUser, UserAdmin)
admin.site.register(CustomerEstablishments)
admin.site.register(CustomerEmail)
admin.site.register(CustomerWeb)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(UserProfile)
admin.site.register(CustomerPhone)
admin.site.register(BasicPhoneCategory, BasicPhoneCategoryAdmin)
admin.site.register(CustomerBankAccount)

admin.site.register(CustomerTranslation)

admin.site.register(Permission)
admin.site.register(PasswordResetLink)
