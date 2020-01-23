from integ.models import (
    OpenId,
)
import uuid

def user_can_modify_open_id(str_open_id, obj_user):
    if obj_user.has_perm('customers.is_poweruser'):
        return True
    uuid_oid = uuid.UUID(str(str_open_id))
    int_obj = OpenId.objects.get(int_id = uuid_oid)
    if int_obj:
        return int_obj.user_can_modify_open_id(obj_user)
    return False

def user_can_acces_open_id(str_open_id, obj_user):
    if obj_user.has_perm('customers.is_poweruser'):
        return True
    uuid_oid = uuid.UUID(str(str_open_id))
    int_obj = OpenId.objects.get(int_id = uuid_oid)
    if int_obj:
        return int_obj.user_can_acces_open_id(obj_user)
    return False

def get_owner_desc(str_open_id, can_modify=False):
    uuid_oid = uuid.UUID(str(str_open_id))
    int_obj = OpenId.objects.get(int_id = uuid_oid)
    if int_obj:
        return int_obj.get_owner_desc(can_modify)
    return None

def get_docs_by_open_id(str_open_id):
    uuid_oid = uuid.UUID(str(str_open_id))
    int_obj = OpenId.objects.get(int_id = uuid_oid)
    if int_obj:
        return int_obj.get_docs()
    return None

"""

"""
