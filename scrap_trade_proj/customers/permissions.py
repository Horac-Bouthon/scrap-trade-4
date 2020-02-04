#
#  Permission Mixins and Decorators
#

# @todo; Instead of 403 on PermissionDenied, set up a friendlier page
# @todo; Replace permissions in other apps to these ones, eliminate decorators.py


from django.contrib.auth.mixins import (
    UserPassesTestMixin, 
    PermissionRequiredMixin,
)
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required  # @unused;

# For decorators that don't have access to models from `self`
from .models import Customer




# Simple testing function, for additional context conditionals
def test_poweruser(user):
    # ALWAYS! Check if it's a logged in user at the start otherwise
    # we'll raise user get-attribute errors instead of PermissionDenied
    # exceptions.
    if not user.is_authenticated: 
        return False  
    
    # ALWAYS! Check that superuser passes through as well!
    return user.has_perm('customers.is_poweruser') or user.is_superuser


# Django Mixin, for class-based view inheritance
class Poweruser(UserPassesTestMixin):
    def test_func(self):
        return test_poweruser(self.request.user)


# Django decorator, for view functions
def poweruser(function):
    def wrap(request, *args, **kwargs):
        if test_poweruser(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def test_user_belong_customer(user, customer):
    if not user.is_authenticated: 
        return False
    belong = customer == user.customer
    power = test_poweruser(user)
    return belong or power or user.is_superuser

class UserBelongCustomer(UserPassesTestMixin):
    def test_func(self):
        customer = self.get_object()  # Can raise exception if model != Customer
        return test_user_belong_customer(self.request.user, customer)
    
def user_belong_customer(function):
    def wrap(request, *args, **kwargs):
        customer = Customer.objects.get(id = kwargs['pk'])  # @todo; Change these get() and filter().first() calls to `django.shortcuts.get_object_or_404()`; We don't want the server to raise DB exceptions, who knows what it'll do in production.
        if test_user_belong_customer(request.user, customer):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def test_can_edit_customer(user, customer): 
    if not user.is_authenticated: 
        return False
    belong = customer == user.customer
    admin = user.has_perm('customers.is_customer_admin')
    power = test_poweruser(user)
    return (belong and admin) or power or user.is_superuser

class CanEditCustomer(UserPassesTestMixin):
    def test_func(self):
        customer = self.get_object()
        return test_can_edit_customer(self.request.user, customer)
    
def can_edit_customer(function):
    def wrap(request, *args, **kwargs):
        customer = Customer.objects.filter(id = kwargs['pk']).first()
        if test_can_edit_customer(request.user, customer):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
