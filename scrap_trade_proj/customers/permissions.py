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
from django.contrib.auth.decorators import login_required

# For decorators that don't have access to models from `self`
from .models import Customer



# Simple testing function, for additional context conditionals
def test_user_belong_customer(user, customer):
    if not user.is_authenticated: 
        return False
    belong = customer == user.customer
    power = user.has_perm("customers.is_poweruser")
    return belong or power

# Django Mixin, for class-based view inheritance
class UserBelongCustomer(UserPassesTestMixin):
    def test_func(self):
        customer = self.get_object()  # Can raise exception if model != Customer
        return test_user_belong_customer(self.request.user, customer)
    
# Django decorator, for view functions
def user_belong_customer(function): 
    def wrap(request, *args, **kwargs):
        customer = Customer.objects.filter(id = kwargs['pk']).first()
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
    power = user.has_perm("customers.is_poweruser")
    return (belong and admin) or power    

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



def test_poweruser(user):
    if not user.is_authenticated: 
        return False
    return user.has_perm('customers.is_poweruser')

class Poweruser(PermissionRequiredMixin): 
    permission_required = 'customers.is_poweruser'
    
def poweruser(function):
    @login_required
    def wrap(request, *args, **kwargs):
        if test_poweruser(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
