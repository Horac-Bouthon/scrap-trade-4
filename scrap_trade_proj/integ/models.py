from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr
from doc_repo.modules.doc_repo_mod import OwnerDescription
import uuid

# Create your models here.
class OpenId(models.Model):
    int_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_('open id'),
        help_text=_("Open key to connect loose parts."),
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('OpenId definition', 'Open id')
        verbose_name_plural = tr.pgettext_lazy('OpenId definition', 'Open ids')

    def __str__(self):
        return str(self.int_id)

    def get_as_string(self):
        return str(self.int_id)

    def get_docs(self):
        return self.my_docs.all().order_by('-id')

    def get_owner_desc(self, can_modify=False):
        if self.my_offers.all().count() > 0:
            if can_modify:
                str_url_key = 'ah-offer-detail'
            else:
                str_url_key = 'ah-offer-info'
            for offer in self.my_offers.all():
                return OwnerDescription(str_url_key, offer.description, offer.pk)
            return None
        if self.my_offer_lines.all().count() > 0:
            if can_modify:
                str_url_key = 'ah-offer-detail'
            else:
                str_url_key = 'ah-offer-info'
            for line in self.my_offer_lines.all():
                return OwnerDescription(str_url_key, line.description, line.offer.pk)
            return None
        if self.my_answers.all().count() > 0:
            if can_modify:
                str_url_key = 'ah-answer-detail'
            else:
                str_url_key = 'ah-answer-info'
            for answer in self.my_answers.all():
                return OwnerDescription(str_url_key, answer.description, answer.pk)
            return None
        if self.my_user_profs.all().count() > 0:
            for profile in self.my_user_profs.all():
                return OwnerDescription('user-profile', profile.user.email)
            return None
        if self.my_estab.all().count() > 0:
            if can_modify:
                str_url_key = 'project-customer-detail'
            else:
                str_url_key = 'project-customer-info'
            for est in self.my_estab.all():
                return OwnerDescription(str_url_key, est.establishment, est.customer.pk)
            return None
        if self.my_customers.all().count() > 0:
            if can_modify:
                str_url_key = 'project-customer-detail'
            else:
                str_url_key = 'project-customer-info'
            for cust in self.my_customers.all():
                return OwnerDescription(str_url_key, cust.customer_name, cust.pk)
            return None
        return None

    def user_can_acces_open_id(self, obj_user):
        if self.my_offers.all().count() > 0:
            for offer in self.my_offers.all():
                for user in offer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
                for s_obj in offer.offered_to.all():
                    for s_user in s_obj.projectcustomuser_set.all():
                        if s_user == obj_user:
                            return True
            return False
        if self.my_offer_lines.all().count() > 0:
            for line in self.my_offer_lines.all():
                for user in line.offer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
                for s_obj in line.offer.offered_to.all():
                    for s_user in s_obj.projectcustomuser_set.all():
                        if s_user == obj_user:
                            return True
            return False
        if self.my_answers.all().count() > 0:
            for answer in self.my_answers.all():
                for user in answer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
                for s_user in answer.ah_offer.owner.projectcustomuser_set.all():
                    if s_user == obj_user:
                        return True
            return False
        if self.my_user_profs.all().count() > 0:
            return True
        if self.my_estab.all().count() > 0:
            return True
        if self.my_customers.all().count() > 0:
            return True
        return False

    def user_can_modify_open_id(self, obj_user):
        if self.my_offers.all().count() > 0:
            for offer in self.my_offers.all():
                for user in offer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
            return False

        if self.my_offer_lines.all().count() > 0:
            for line in self.my_offer_lines.all():
                for user in line.offer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
            return False

        if self.my_answers.all().count() > 0:
            for answer in self.my_answers.all():
                for user in answer.owner.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
            return False

        if self.my_customers.all().count() > 0:
            for cust in self.my_customers.all():
                for user in cust.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
            return False

        if self.my_estab.all().count() > 0:
            for est in self.my_estab.all():
                for user in est.customer.projectcustomuser_set.all():
                    if user == obj_user:
                        return True
            return False

        if self.my_user_profs.all().count() > 0:
            for profile in self.my_user_profs.all():
                return profile.user == obj_user
            return False

        return False
