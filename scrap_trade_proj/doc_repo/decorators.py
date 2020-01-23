from django.core.exceptions import PermissionDenied
from doc_repo.models import Document
from integ.modules.integ_modules import (
    user_can_modify_open_id,
    user_can_acces_open_id,
)

def user_can_modify_owner_obj(function):
    def wrap(request, *args, **kwargs):
        if 'oid' in kwargs:
            str_oid = kwargs["oid"]
        else:
            if 'pk' in kwargs:
                pk = kwargs["pk"]
                doc = Document.objects.get(id = pk)
                if doc == None:
                    raise PermissionDenied
                str_oid = str(doc.open_id.get_as_string())
            else:
                raise PermissionDenied
        if user_can_modify_open_id(str_oid, request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_can_access_owner_obj(function):
    def wrap(request, *args, **kwargs):
        if 'oid' in kwargs:
            str_oid = kwargs["oid"]
        else:
            if 'pk' in kwargs:
                pk = kwargs["pk"]
                doc = Document.objects.get(id = pk)
                if doc == None:
                    raise PermissionDenied
                str_oid = str(doc.open_id.get_as_string())
            else:
                raise PermissionDenied
        if user_can_acces_open_id(str_oid, request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
