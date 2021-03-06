#
#  Permission Mixins and Decorators
#


from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.core.exceptions import PermissionDenied


from customers.permissions import test_poweruser, test_user_belong_customer
from .models import AhOffer, AhAnswer




def test_user_belong_offer(user, offer):  # Test func
    return test_user_belong_customer(user, offer.owner)

class UserBelongOffer(UserPassesTestMixin):  # Interface
    def test_func(self):
        offer = self.get_object()
        return test_user_belong_offer(self.request.user, offer)

def user_belong_offer(function):  # Decorator
    def wrap(request, *args, **kwargs):
        
        offer = AhOffer.objects.get(id = kwargs['pk'])
        
        if test_user_belong_offer(request.user, offer):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap




def test_user_belong_answer(user, answer):  # Test func
    return test_user_belong_customer(user, answer.owner)


class UserBelongAnswer(UserPassesTestMixin):  # Interface
    def test_func(self):
        answer = self.get_object()
        return test_user_belong_answer(self.request.user, answer)

def user_belong_answer(function):  # Decorator
    def wrap(request, *args, **kwargs):
        answer = AhAnswer.objects.get(id = kwargs['pk'])
        if test_user_belong_answer(request.user, answer):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
