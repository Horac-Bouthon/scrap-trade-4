from django.core.exceptions import PermissionDenied
from customers.models import Customer

def user_belong_customer(function):
    def wrap(request, *args, **kwargs):
        customer = Customer.objects.filter(id = kwargs['pk']).first()
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
