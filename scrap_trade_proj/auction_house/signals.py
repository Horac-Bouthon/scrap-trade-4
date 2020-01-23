from django.db.models.signals import pre_save, post_delete
from .models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
)
from integ.models import OpenId
from django.dispatch import receiver
import uuid

@receiver(pre_save, sender=AhOffer)
def offer_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=AhOffer)
def offer_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()

@receiver(pre_save, sender=AhOfferLine)
def offer_line_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=AhOfferLine)
def offer_line_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()

@receiver(pre_save, sender=AhAnswer)
def answer_save(sender, instance, **kwargs):
    if instance.open_id == None:
        new_id = OpenId()
        new_id.save()
        instance.open_id = new_id

@receiver(post_delete, sender=AhAnswer)
def answer_clean(sender, instance, **kwargs):
    if instance.open_id != None:
        uuid_var = uuid.UUID(str(instance.open_id))
        obj = OpenId.objects.get(int_id = uuid_var)
        obj.delete()
