from django.db.models.signals import pre_delete
from customers.models import UserProfile
from integ.models import OpenId
from django.dispatch import receiver
