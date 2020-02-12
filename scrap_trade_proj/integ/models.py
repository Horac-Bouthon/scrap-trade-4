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
    
    
    def get_docs(self, max=-1):
        if max >= 0:
            rv = self.my_docs.all().order_by('-id')[:max]
        else:
            rv = self.my_docs.all().order_by('-id')
        return rv

    
    def get_owner_desc(self, can_modify=False):
        """
        What does this OpenID belong to? Let's try checking
        all possibilities, one by one.
        """
        
        url_key = 'ah-offer-detail' if can_modify else 'ah-offer-info'
        offer = self.my_offers.first()
        if offer:
            return OwnerDescription(url_key, 
                                    offer.description, offer.pk)
        line = self.my_offer_lines.first()
        if line:
            return OwnerDescription(url_key, 
                                    line.description, line.offer.pk)
        
        answer = self.my_answers.first()
        if answer:
            url_key = 'ah-answer-detail' if can_modify else 'ah-answer-info'
            return OwnerDescription(url_key,
                                    answer.description, answer.pk)
        
        profile = self.my_user_profs.first()
        if profile:
            url_key = 'user-profile'
            return OwnerDescription(url_key,
                                    profile.user.email)
        
        estab = self.my_estab.first()
        if estab:
            url_key = 'project-customer-detail' if can_modify else 'project-customer-info'
            return OwnerDescription(
                url_key, 
                estab.establishment, estab.customer.pk
            )
        
        customer = self.my_customers.first()
        if customer:
            url_key = 'project-customer-detail' if can_modify else 'project-customer-info'
            return OwnerDescription(url_key, 
                                    customer.customer_name, customer.pk)
        
        # The rare case that it doesn't belong to anyone
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
