from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr
import uuid


class OwnerDescription:

    def __init__(self,
                 url_key,
                 desc='Owner',
                 obj_pk=None,
                 ):
        self.url_key = url_key
        self.obj_pk = obj_pk
        self.desc = desc

    def __repr__(self):
        return "OwnerDescription('{}', '{}', {})"\
            .format(self.url_key, self.desc, self.obj_pk)

    def __str__(self):
        return "{} {} {} {}"\
            .format(self.pk, self.url_key, url.desc, self.obj_pk)

    @property
    def url_command(self):
        if self.obj_pk != None:
                return reverse(self.url_key, args=(self.obj_pk, ))
        return reverse(self.url_key)
