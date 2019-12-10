from django.core.exceptions import PermissionDenied
from customers.models import Customer
from . models import AhOffer, AhAnswer

def user_belong_offer(function):
    def wrap(request, *args, **kwargs):
        id = kwargs["pk"]
        offer = AhOffer.objects.get(id = id)
        customer = offer.owner
        co1 = request.user.is_superuser
        co2 = request.user.has_perm('customers.is_poweruser')
        co3 = customer == request.user.customer
        if co1 or co2 or co3:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_belong_answer(function):
    def wrap(request, *args, **kwargs):
        id = kwargs["pk"]
        answer = AhAnswer.objects.get(id = id)
        customer = answer.owner
        co1 = request.user.is_superuser
        co2 = request.user.has_perm('customers.is_poweruser')
        co3 = customer == request.user.customer
        if co1 or co2 or co3:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_corespond_customer(function):
    def wrap(request, *args, **kwargs):
        offer = AhOffer.objects.filter(id = kwargs['pk']).first()
        customer = offer.owner
        co1 = request.user.is_superuser
        co2 = request.user.has_perm('customers.is_poweruser')
        co3 = customer == request.user.customer
        if co1 or co2 or co3:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
