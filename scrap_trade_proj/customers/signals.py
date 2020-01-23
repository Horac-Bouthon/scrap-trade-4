from django.db.models.signals import pre_save, post_save, post_delete
from .models import (
    ProjectCustomUser,
    UserProfile,
    CustomerEstablishments,
    Customer,
)
from integ.models import OpenId
from django.dispatch import receiver
import uuid

@receiver(post_save, sender=ProjectCustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=ProjectCustomUser)
def user_save(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(pre_save, sender=UserProfile)
def profile_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=UserProfile)
def profile_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()

@receiver(pre_save, sender=CustomerEstablishments)
def estab_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=CustomerEstablishments)
def estab_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()

@receiver(pre_save, sender=Customer)
def customer_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=Customer)
def customer_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()
