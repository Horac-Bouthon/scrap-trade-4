from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from customers.models import ProjectCustomUser as User

poweruser, created = Group.objects.get_or_create(name ='poweruser')
customer_admin, created = Group.objects.get_or_create(name ='customer_admin')
customer_worker, created = Group.objects.get_or_create(name ='customer_worker')

ct = ContentType.objects.get_for_model(User)

f1 = Permission.objects.filter(codename = 'is_poweruser')
if f1.count() > 0:
    permission1 = f1.first()
else:
    permission1 = Permission.objects.create(codename = 'is_poweruser', name ='custom - poweruser', content_type = ct)

f2 = Permission.objects.filter(codename = 'is_customer_admin')
if f2.count() > 0:
    permission2 = f2.first()
else:
    permission2 = Permission.objects.create(codename = 'is_customer_admin', name ='custom - customer-admin', content_type = ct)

f3 = Permission.objects.filter(codename = 'is_customer_user')
if f3.count() > 0:
    permission3 = f3.first()
else:
    permission3 = Permission.objects.create(codename = 'is_customer_user', name ='custom - customer-user', content_type = ct)

pu1 = poweruser.permissions.filter(codename = 'is_poweruser')
if pu1.count() < 1:
    poweruser.permissions.add(permission1)
pu2 = poweruser.permissions.filter(codename = 'is_customer_admin')
if pu2.count() < 1:
    poweruser.permissions.add(permission2)
pu3 = poweruser.permissions.filter(codename = 'is_customer_user')
if pu3.count() < 1:
    poweruser.permissions.add(permission3)

pu2 = customer_admin.permissions.filter(codename = 'is_customer_admin')
if pu2.count() < 1:
    customer_admin.permissions.add(permission2)
pu3 = customer_admin.permissions.filter(codename = 'is_customer_user')
if pu3.count() < 1:
    customer_admin.permissions.add(permission3)


pu3 = customer_worker.permissions.filter(codename = 'is_customer_user')
if pu3.count() < 1:
    customer_worker.permissions.add(permission3)
