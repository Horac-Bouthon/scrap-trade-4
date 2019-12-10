from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime
from .decorators import user_belong_offer, user_corespond_customer, user_belong_answer
from customers.decorators import user_belong_customer
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import (
    AhOffer,
    AhOfferLine,
    AhMatClass,
    AhAnswer,
    AhAnswerLine,
)
from customers.models import (
    Customer,
)
from project_main.models import Project

from .forms import (
    AhOfferLineUpdateForm,
    AhOfferUpdateForm,
    AhAnwserLinePpuUpdateForm,
    AhAnwserLineTotalUpdateForm,
    AhAnwserCreateForm,
)

from django.utils import translation as tr
from django.utils.translation import gettext as _
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

class AhOfferListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_list.html'
    context_object_name = 'offers'
    ordering = ['-pk']
    permission_required = 'customers.is_poweruser'


class AhOfferDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = AhOffer

    def test_func(self):
        offer = self.get_object()
        customer = offer.owner
        co1 = self.request.user.is_superuser
        co2 = self.request.user.has_perm('customers.is_poweruser')
        co3 = self.request.user.customer == customer
        return co1 or co2 or co3

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        context['my_answers'] = object.answers.filter(is_confirmed = True,
            is_closed = False, is_cancelled = False).order_by('-total_price')[:5]
        context['bound_answers'] = object.answers.filter(is_bound = True)
        context['answers_total'] = object.answers.filter(is_confirmed = True,
            is_closed = False, is_cancelled = False).count()

        return context

class AhOfferInfoView(LoginRequiredMixin, DetailView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_info.html'

class AhOfferUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AhOffer
    fields = ['description', 'delivery_date', 'auction_date',
        'is_new', 'is_confirmed', 'confirmed_at', 'is_accepted', 'accepted_at',
        'is_ready_close', 'ready_close_at',
        'is_closed', 'closed_at', 'is_cancelled', 'canceled_at', 'offered_to',
    ]
    permission_required = 'customers.is_poweruser'

class AhOfferCustomerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AhOffer
    fields = [
        'description', 'delivery_date', 'auction_date',
    ]
    template_name = 'auction_house/ahoffer_customer_form.html'

    def test_func(self):
        offer = self.get_object()
        customer = offer.owner
        co1 = self.request.user.is_superuser
        co2 = self.request.user.has_perm('customers.is_poweruser')
        co3 = self.request.user.customer == customer
        return co1 or co2 or co3


class AhOfferDeletelView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AhOffer
    permission_required = 'customers.is_poweruser'
    success_url = reverse_lazy('ah-offer-list')

#--------------------------------

@login_required()
@user_belong_offer
def ah_offer_line_update(request, pk, pk2):
    offer = AhOffer.objects.filter(id = pk).first()
    offer_line = AhOfferLine.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = AhOfferLineUpdateForm(request.POST, instance=offer_line)
        if form.is_valid():
            form.save()
            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('ah-offer-detail', pk)
    else:
        form = AhOfferLineUpdateForm(instance=offer_line)

    title2 = tr.pgettext('ah_offer_line_update-title', 'update-line')
    context = {
        'form': form,
        'title': title2,
        'offer': offer,
    }
    return render(request, 'auction_house/offer_line_form.html', context)

@login_required()
@user_belong_offer
def ah_offer_line_create(request, pk):
    offer = AhOffer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = AhOfferLineUpdateForm(request.POST)
        if form.is_valid():
            offer.lines.create(
                description = form.cleaned_data['description'],
                amount = form.cleaned_data['amount'],
                mat_class = form.cleaned_data['mat_class'],
                offer = offer,
            )
            success_message = _('Your offer has been added!')
            messages.success(request, success_message)
            return redirect('ah-offer-detail', pk)
    else:
        form = AhOfferLineUpdateForm()

    title2 = tr.pgettext('ah_offer_line_create-title', 'create-offer')
    context = {
        'form': form,
        'title': title2,
        'offer': offer,
    }
    return render(request, 'auction_house/offer_line_form.html', context)


class AhDeletelOfferLine(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AhOfferLine

    def delete(self, *args, **kwargs):
        self.offer_pk = self.get_object().offer.id
        super().delete(*args, **kwargs)
        return redirect('ah-offer-detail', self.object.offer.pk)

    def get_success_url(self):
        return reverse_lazy('ah-offer-detail',  kwargs={'pk': self.offer_pk})

    def test_func(self):
        customer = self.get_object().offer.owner
        co1 = self.request.user.is_superuser
        co2 = self.request.user.has_perm('customers.is_poweruser')
        co3 = self.request.user.customer == customer
        return co1 or co2 or co3


#--------------------------------

class AhMatClassDetailView(LoginRequiredMixin, DetailView):
    model = AhMatClass

def get_waiting_offers(par_customer):
    ret_offers = par_customer.receive_offers.filter(is_confirmed = True)
    for answer in par_customer.owned_answers.all():
        ret_offers = ret_offers.exclude(id = answer.ah_offer.pk)
    return ret_offers.order_by("-pk")


#-------------------------------- ah_customer_auction
@login_required()
@user_belong_customer
def ah_customer_auction(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    title2 = tr.pgettext('ah_customer_auction-title', 'customer-auction')
    context = {
        'title': title2,
        'customer': customer,
        'new_offers': customer.owned_offers.filter(is_new = True),
        'commited_offers': customer.owned_offers.filter(is_confirmed = True),
        'accepted_offers': customer.owned_offers.filter(is_accepted = True),
        'ready_close_offfer': customer.owned_offers.filter(is_ready_close = True),
        'closed_offers': customer.owned_offers.filter(is_closed = True),
        'canceled_offers': customer.owned_offers.filter(is_cancelled = True),
        'new_answers': customer.owned_answers.filter(is_new = True),
        'confirmed_answers': customer.owned_answers.filter(is_confirmed = True),
        'successful_answers': customer.owned_answers.filter(is_successful = True),
        'accepted_answers': customer.owned_answers.filter(is_accepted = True),
        'closed_answers': customer.owned_answers.filter(is_closed = True),
        'cancelled_answers': customer.owned_answers.filter(is_cancelled = True),
        'waiting_offers': get_waiting_offers(customer),
    }
    return render(request, 'auction_house/customer_auction.html', context)

#-------------------------------- offer views
def offer_to(par_customer):
    return Customer.objects.exclude(id = par_customer.pk)

@login_required()
@user_belong_customer
def ah_customer_offers_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    user = request.user

    if request.method == 'POST':
        form = AhOfferUpdateForm(request.POST)
        if form.is_valid():
            new = AhOffer(
                description = form.cleaned_data['description'],
                delivery_date = form.cleaned_data['delivery_date'],
                auction_date = form.cleaned_data['auction_date'],
                is_new = True,
                owner = customer,
                creator = user,
            )
            new.save()
            for cc in offer_to(customer):
                new.offered_to.add(cc)
            new.save()
            success_message = _('Your offer has been added!')
            messages.success(request, success_message)
            return redirect('ah-customer-auction', pk)
    else:
        form = AhOfferUpdateForm()

    title2 = tr.pgettext('ah_customer_offers_create-title', 'create-offer')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
    }
    return render(request, 'auction_house/ahoffer_customer_new.html', context)


@login_required()
@user_belong_customer
def ah_customer_offers_new(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_new-title', 'new-offers')
    context = {
        'title': title2,
        'selection': _('new offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_new = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_confirm(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        offer.is_new = False
        offer.is_confirmed = True
        offer.is_accepted = False
        offer.is_ready_close = False
        offer.is_closed = False
        offer.is_cancelled = False
        offer.confirmed_at = datetime.now()
        offer.save()
        success_message = _('Your offer has been confirmed!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_offers_new-title', 'new-offers')
    context = {
        'title': title2,
        'customer': customer,
        'offer': offer,
    }
    return render(request, 'auction_house/ahoffer_confirm.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_close(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        offer.is_new = False
        offer.is_confirmed = False
        offer.is_accepted = False
        offer.is_ready_close = False
        offer.is_closed = True
        offer.is_cancelled = False
        offer.confirmed_at = datetime.now()
        offer.save()
        success_message = _('Your offer has been closed!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_offers_close-title', 'close-offer')
    context = {
        'title': title2,
        'customer': customer,
        'offer': offer,
    }
    return render(request, 'auction_house/ahoffer_confirm_close.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_cancel(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        offer.is_new = False
        offer.is_confirmed = False
        offer.is_accepted = False
        offer.is_ready_close = False
        offer.is_closed = False
        offer.is_cancelled = True
        offer.confirmed_at = datetime.now()
        offer.save()
        for answer in offer.answers.all():
            answer.is_new = False
            answer.is_confirmed = False
            answer.is_successful = False
            answer.is_bound = False
            answer.is_closed = False
            answer.is_cancelled = True
            answer.save()
        success_message = _('Your offer has been canceled!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_offers_cancel-title', 'cancel-offers')
    context = {
        'title': title2,
        'customer': customer,
        'offer': offer,
    }
    return render(request, 'auction_house/ahoffer_confirm_cancel.html', context)


@login_required()
@user_belong_customer
def ah_customer_offers_commited(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_commited-title', 'commited-offers')
    context = {
        'title': title2,
        'selection': _('commited offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_confirmed = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_accepted(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_closed-title', 'accepted-offers')
    context = {
        'title': title2,
        'selection': _('accepted offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_accepted = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_ready_close(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_ready_close-title', 'ready-to-close-offers')
    context = {
        'title': title2,
        'selection': _('ready to close offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_ready_close = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)


@login_required()
@user_belong_customer
def ah_customer_offers_closed(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_closed-title', 'closed-offers')
    context = {
        'title': title2,
        'selection': _('closed offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_closed = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_offers_canceled(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offers_canceled-title', 'canceled-offers')
    context = {
        'title': title2,
        'selection': _('canceled offers'),
        'customer': customer,
        'offer_list': customer.owned_offers.filter(is_cancelled = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

#-------------------------------- answer views
class AhAnswerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AhAnswer
    template_name = 'auction_house/ahanswer_list.html'
    context_object_name = 'answers'
    ordering = ['-pk']
    permission_required = 'customers.is_poweruser'


class AhAnswerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = AhAnswer
    template_name = 'auction_house/ahanswer_detail.html'

    def test_func(self):
        answer = self.get_object()
        customer = answer.owner
        co1 = self.request.user.is_superuser
        co2 = self.request.user.has_perm('customers.is_poweruser')
        co3 = self.request.user.customer == customer
        return co1 or co2 or co3

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        object = kwargs.get('object')
        if object.is_new or object.is_confirmed:
            can = self.request.user.has_perm('customers.is_poweruser')
        else:
            can = False
        context['power_can_change'] = can
        return context


class AhAnswerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AhAnswer
    fields = [
        'description',
        'owner',
        'ah_offer',
        'total_price',
        'is_new',
        'is_confirmed',
        'confirmed_at',
        'is_successful',
        'is_bound',
        'is_accepted',
        'accepted_at',
        'is_closed',
        'closed_at',
        'is_cancelled',
        'canceled_at',
    ]
    permission_required = 'customers.is_poweruser'


class AhAnswerCustomerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AhAnswer
    fields = [
        'description',
    ]
    template_name = 'auction_house/ahanswer_customer_form.html'

    def test_func(self):
        offer = self.get_object()
        customer = offer.owner
        co1 = self.request.user.is_superuser
        co2 = self.request.user.has_perm('customers.is_poweruser')
        co3 = self.request.user.customer == customer
        return co1 or co2 or co3


class AhAnswerDeletelView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = AhAnswer
    permission_required = 'customers.is_poweruser'
    success_url = reverse_lazy('ah-answer-list')


@login_required()
@user_belong_customer
def ah_customer_answer_waiting_offers(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_new-title', 'new-answers')
    context = {
        'title': title2,
        'selection': _('waiting offer'),
        'customer': customer,
        'offer_list': get_waiting_offers(customer),
    }
    return render(request, 'auction_house/customer_waiting_list.html', context)


@login_required()
@user_belong_customer
def ah_customer_answer_new(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_new-title', 'new-answers')
    context = {
        'title': title2,
        'selection': _('new answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_new = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_confirmed(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_confirmed-title', 'confirmed-answers')
    context = {
        'title': title2,
        'selection': _('confirmed answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_confirmed = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_successful(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_successful-title', 'successful-answers')
    context = {
        'title': title2,
        'selection': _('successful answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_successful = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_accepted(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_accepted-title', 'accepted-answers')
    context = {
        'title': title2,
        'selection': _('accepted answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_accepted = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_closed(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_closed-title', 'closed-answers')
    context = {
        'title': title2,
        'selection': _('closed answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_closed = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_cancelled(request, pk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_cancelled-title', 'cancelled-answers')
    context = {
        'title': title2,
        'selection': _('cancelled answers'),
        'customer': customer,
        'answer_list': customer.owned_answers.filter(is_cancelled = True).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_create(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()
    user = request.user

    if request.method == 'POST':
        form = AhAnwserCreateForm(request.POST)
        if form.is_valid():
            new = AhAnswer(
                description = form.cleaned_data['description'],
                owner = customer,
                ah_offer = offer,
                is_new = True,
                creator = user,
                changed_by = user,
            )
            new.save()
            for line in offer.lines.all():
                n_a_l = AhAnswerLine(
                    answer = new,
                    offer_line = line,
                )
                n_a_l.save()
            success_message = _('Your answer has been added!')
            messages.success(request, success_message)
            return redirect('ah-customer-auction', pk)
    else:
        form = AhAnwserCreateForm()

    title2 = tr.pgettext('ah_customer_answer_create-title', 'create-answer')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
        'offer': offer,
    }
    return render(request, 'auction_house/ahanswer_customer_new.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_confirm(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    answer = AhAnswer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        answer.is_new = False
        answer.is_confirmed = True
        answer.is_accepted = False
        answer.is_closed = False
        answer.is_successful = False
        answer.is_cancelled = False
        answer.confirmed_at = datetime.now()
        answer.changed_by = request.user
        answer.save()
        success_message = _('Your answer has been confirmed!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_answer_confirm-title', 'confirm-offer')
    context = {
        'title': title2,
        'customer': customer,
        'answer': answer,
    }
    return render(request, 'auction_house/ahanswer_confirm.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_accept(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    answer = AhAnswer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        my_now = datetime.now()
        answer.is_new = False
        answer.is_confirmed = False
        answer.is_accepted = True
        answer.is_closed = False
        answer.is_successful = False
        answer.is_cancelled = False
        answer.accepted_at = my_now
        answer.changed_by = request.user
        answer.save()
        answer.ah_offer.is_new = False
        answer.ah_offer.is_confirmed = False
        answer.ah_offer.is_accepted = True
        answer.ah_offer.is_ready_close = False
        answer.ah_offer.is_closed = False
        answer.ah_offer.is_cancelled = False
        answer.ah_offer.accepted_at = my_now
        answer.ah_offer.save()
        success_message = _('Your answer has been accepted!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_answer_accept-title', 'accept-offer')
    context = {
        'title': title2,
        'customer': customer,
        'answer': answer,
    }
    return render(request, 'auction_house/ahanswer_confirm_accept.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_cancel(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    answer = AhAnswer.objects.filter(id = pk2).first()

    if request.method == 'POST':
        answer.is_new = False
        answer.is_confirmed = False
        answer.is_accepted = False
        answer.is_closed = False
        answer.is_successful = False
        answer.is_bound = False
        answer.is_cancelled = True
        answer.canceled_at = datetime.now()
        answer.changed_by = request.user
        answer.save()
        success_message = _('Your answer has been canceled!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_answer_cancell-title', 'cancel-offer')
    context = {
        'title': title2,
        'customer': customer,
        'answer': answer,
    }
    return render(request, 'auction_house/ahanswer_confirm_cancel.html', context)

@login_required()
@user_belong_customer
def ah_customer_answer_close(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    answer = AhAnswer.objects.filter(id = pk2).first()
    my_now = datetime.now()

    if request.method == 'POST':
        answer.is_new = False
        answer.is_confirmed = False
        answer.is_accepted = False
        answer.is_closed = True
        answer.is_successful = False
        answer.is_cancelled = False
        answer.closed_at = my_now
        answer.changed_by = request.user
        answer.save()
        answer.ah_offer.is_new = False
        answer.ah_offer.is_confirmed = False
        answer.ah_offer.is_accepted = False
        answer.ah_offer.is_ready_close = True
        answer.ah_offer.is_closed = False
        answer.ah_offer.is_cancelled = False
        answer.ah_offer.accepted_at = my_now
        answer.ah_offer.save()
        success_message = _('Your answer has been closed!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_customer_answer_close-title', 'close-offer')
    context = {
        'title': title2,
        'customer': customer,
        'answer': answer,
    }
    return render(request, 'auction_house/ahanswer_confirm_close.html', context)


@login_required()
@user_belong_answer
def ah_answer_line_update_ppu(request, pk, pk2):
    answer = AhAnswer.objects.filter(id = pk).first()
    answer_line = AhAnswerLine.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = AhAnwserLinePpuUpdateForm(request.POST, instance=answer_line)
        if form.is_valid():
            form.save()
            answer_line = AhAnswerLine.objects.filter(id = pk2).first()
            answer_line.total_price = answer_line.ppu * answer_line.offer_line.amount
            answer_line.save()
            sum = 0
            answer = AhAnswer.objects.filter(id = pk).first()
            for line in answer.my_lines.all():
                sum += line.total_price
            answer.total_price = sum
            answer.save()
            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('ah-answer-detail', pk)
    else:
        form = AhAnwserLinePpuUpdateForm(instance=answer_line)

    title2 = tr.pgettext('ah_answer_line_update-title', 'update-line')
    context = {
        'form': form,
        'title': title2,
        'answer': answer,
    }
    return render(request, 'auction_house/answer_line_form.html', context)

@login_required()
@user_belong_answer
def ah_answer_line_update_total(request, pk, pk2):
    answer = AhAnswer.objects.filter(id = pk).first()
    answer_line = AhAnswerLine.objects.filter(id = pk2).first()

    if request.method == 'POST':
        form = AhAnwserLineTotalUpdateForm(request.POST, instance=answer_line)
        if form.is_valid():
            form.save()
            answer_line = AhAnswerLine.objects.filter(id = pk2).first()
            answer_line.ppu = answer_line.total_price / answer_line.offer_line.amount
            answer_line.save()
            sum = 0
            answer = AhAnswer.objects.filter(id = pk).first()
            print(answer)
            print(answer.my_lines.count())
            for line in answer.my_lines.all():
                print(line.pk)
                sum += line.total_price
            answer.total_price = sum
            answer.save()
            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('ah-answer-detail', pk)
    else:
        form = AhAnwserLineTotalUpdateForm(instance=answer_line)

    title2 = tr.pgettext('ah_answer_line_update-title', 'update-line')
    context = {
        'form': form,
        'title': title2,
        'answer': answer,
    }
    return render(request, 'auction_house/answer_line_form.html', context)
