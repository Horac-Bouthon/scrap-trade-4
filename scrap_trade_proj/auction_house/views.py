from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.template import Context
from django.db.models import Q
from datetime import datetime
from django.urls import reverse_lazy, reverse

from .modules.auction import (
    resurect_auction,
    set_auction,
    customer_offer_create,
    offer_add_state,
    fiter_by_state,
    customer_answer_create,
    answer_add_state,
    get_waiting_offers,
    get_auction_list_control_obj,
)
from .modules.ntf_support import send_ntf_from_state

from state_wf.models import (
    Step,
    StepState,
)

from .decorators import (
    # @todo; Add `permissions.py` to this app and simplify auth
    user_belong_offer,
    user_corespond_customer,
    user_belong_answer,
)
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
    StepUpdateForm,
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
        context['my_answers'] = fiter_by_state(object.answers, 'answer_confirmed').order_by('-total_price')[:5]
        context['bound_answers'] = object.answers.filter(is_bound = True)
        context['answers_total'] = fiter_by_state(object.answers, 'answer_confirmed').count()
        context['state_new'] = StepState.objects.get(state_key='offer_new')
        context['state_confirmed'] = StepState.objects.get(state_key='offer_confirmed')
        context['state_accepted'] = StepState.objects.get(state_key='offer_accepted')
        context['state_ready_to_close'] = StepState.objects.get(state_key='offer_ready_to_close')
        context['state_closed'] = StepState.objects.get(state_key='offer_closed')

        object.refresh_total_price()

        return context

class AhOfferInfoView(LoginRequiredMixin, DetailView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_info.html'


class AhOfferUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AhOffer
    fields = ['description', 'delivery_date', 'auction_date',
        'minimal_total_price', 'auction_url', 'auction_start',
        'auction_end', 'offered_to',
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
            offer.refresh_total_price()
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
                minimal_ppu = form.cleaned_data['minimal_ppu'],
                offer = offer,
            )
            offer.refresh_total_price()
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

#-------------------------------- ah_customer_auction
@login_required()
@user_belong_customer
def ah_customer_auction(request, pk):
    customer = Customer.objects.get(id = pk)

    auc_obj = get_auction_list_control_obj(customer, customer.owned_offers, customer.owned_answers)

    title2 = tr.pgettext('ah_customer_auction-title', 'customer-auction')
    context = {
        'title': title2,
        'customer': customer,
        'auc_obj': auc_obj,
    }

    context['content_header'] = {
        'title': customer.customer_name + ' | ' + _('Auction'),
        'desc': _('Auction homepage'),
        'image': { 'src': customer.customer_logo.url,
                   'alt': _('Customer logo') },
        'button_list': [
            {
                'text': _("Create new offer"),
                'href': reverse('ah-customer-create-offers',
                                kwargs={'pk': customer.pk}),
                'icon': 'plus',
            }, {
                'text': _("Edit customer info"),
                'href': reverse('project-customer-detail',
                                kwargs={'pk': customer.pk}),
                'icon': 'edit-3',
            }
        ]
    }

    return render(request, 'auction_house/customer_auction.html', context)


@login_required()
@user_belong_customer
def ah_customer_offers_create(request, pk):
    customer = Customer.objects.filter(id = pk).first()

    if request.method == 'POST':
        form = AhOfferUpdateForm(request.POST)
        if form.is_valid():
            customer_offer_create(
                customer = customer,
                user = request.user,
                data = form.cleaned_data
            )
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
def ah_customer_offers_by_state_key(request, pk, sk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_offer_by_state_key-title', 'offers-by-state')
    selected_state = StepState.objects.filter(state_key = sk).first()
    context = {
        'title': title2,
        'selection': selected_state.get_state_name_plural(),
        'customer': customer,
        'offer_list': fiter_by_state(customer.owned_offers, sk).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_offer_list.html', context)

@login_required()
@user_belong_customer
def ah_offers_change_state(request, pk, pk2, pk3):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()
    set_state = StepState.objects.get(id=pk3)

    if request.method == 'POST':
        offer_add_state(offer, set_state, request.user)
        if set_state.state_key == 'offer_canceled':
            state_send = StepState.objects.get(state_key = 'answer_canceled')
            my_answers = fiter_by_state(offer.answers, 'answer_confirmed')
            for answer in my_answers.all():
                answer_add_state(answer, state_send, request.user)

        if set_state.send_ntf:
            context = Context()
            context['place'] = 'auction_house.view - ah_offers_change_state()'
            context['item'] = offer
            send_ntf_from_state(request, set_state, context)

        success_message = _('Your offer has change the state!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_offers_change_state-title', 'offer-state')
    context = {
        'title': title2,
        'customer': customer,
        'offer': offer,
        'state': set_state,
    }
    return render(request, 'auction_house/ahoffer_change_state.html', context)

@login_required()
@user_belong_customer
def ah_answer_change_state(request, pk, pk2, pk3):
    customer = Customer.objects.filter(id = pk).first()
    answer = AhAnswer.objects.filter(id = pk2).first()
    set_state = StepState.objects.get(id=pk3)

    if request.method == 'POST':
        answer_add_state(answer, set_state, request.user)
        if set_state.state_key == 'answer_accepted':
            state_send = StepState.objects.get(state_key = 'offer_accepted')
            offer_add_state(answer.ah_offer, state_send, request.user)
            if state_send.send_ntf:
                context = Context()
                context['place'] = 'auction_house.view - ah_answer_change_state() - answer_accepted'
                context['item'] = answer.ah_offer
                send_ntf_from_state(request, state_send, context)
        if set_state.state_key == 'answer_closed':
            state_send = StepState.objects.get(state_key = 'offer_ready_to_close')
            offer_add_state(answer.ah_offer, state_send, request.user)
            if state_send.send_ntf:
                context = Context()
                context['place'] = 'auction_house.view - ah_answer_change_state() - answer_closed'
                context['item'] = answer.ah_offer
                send_ntf_from_state(request, state_send, context)
        if set_state.state_key == 'answer_canceled' and answer.is_bound:
            resurect_auction(answer.ah_offer)
            set_auction(request, answer.ah_offer)
        success_message = _('Your answer has change the state!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    title2 = tr.pgettext('ah_answer_change_state-title', 'offer-state')
    context = {
        'title': title2,
        'customer': customer,
        'answer': answer,
        'state': set_state,
    }
    return render(request, 'auction_house/ahanswer_change_state.html', context)

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
        state_new = StepState.objects.get(state_key='answer_new')
        state_confirmed = StepState.objects.get(state_key='answer_confirmed')
        context['state_new'] = state_new
        context['state_confirmed'] = state_confirmed
        context['state_successful'] = StepState.objects.get(state_key='answer_successful')
        context['state_accepted'] = StepState.objects.get(state_key='answer_accepted')
        context['state_closed'] = StepState.objects.get(state_key='answer_closed')
        context['state_canceled'] = StepState.objects.get(state_key='answer_canceled')
        object.refresh_total_price()
        return context


class AhAnswerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = AhAnswer
    fields = [
        'description',
        'owner',
        'ah_offer',
        'is_bound',
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
    title2 = tr.pgettext('ah_customer_answer_waiting_offers-title', 'offers_waiting')
    context = {
        'title': title2,
        'selection': _('waiting offer'),
        'customer': customer,
        'offer_list': get_waiting_offers(customer),
    }
    return render(request, 'auction_house/customer_waiting_list.html', context)


@login_required()
@user_belong_customer
def ah_customer_answer_by_state_key(request, pk, sk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_by_state_key-title', 'answers-by-state')
    selected_state = StepState.objects.filter(state_key = sk).first()
    context = {
        'title': title2,
        'selection': selected_state.get_state_name_plural(),
        'customer': customer,
        'answer_list': fiter_by_state(customer.owned_answers, sk).order_by('-pk'),
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
            customer_answer_create(customer, offer, user, form.cleaned_data)
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
        'min_price': answer_line.offer_line.minimal_ppu,
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
            for line in answer.my_lines.all():
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

@login_required()
@permission_required('customers.is_poweruser')
def ah_offer_step_create(request, pk):
    offer = AhOffer.objects.get(id = pk)
    customer = offer.owner

    if request.method == 'POST':
        form = StepUpdateForm(request.POST)
        if form.is_valid():
            new = Step(
                state = form.cleaned_data['state'],
                offer_link = offer,
                answer_link = None,
                changed_by = request.user,
            )
            new.save()
            success_message = _('Step has been added!')
            messages.success(request, success_message)
            return redirect('ah-offer-update', pk)
    else:
        form = StepUpdateForm()

    title2 = tr.pgettext('ah_offer_step_create-title', 'create-step')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
        'object': offer,
        'update_url': 'ah-offer-update',
    }
    return render(request, 'auction_house/ah_step_new.html', context)

@login_required()
@permission_required('customers.is_poweruser')
def ah_answer_step_create(request, pk):
    answer = AhAnswer.objects.get(id = pk)
    customer = answer.owner

    if request.method == 'POST':
        form = StepUpdateForm(request.POST)
        if form.is_valid():
            new = Step(
                state = form.cleaned_data['state'],
                offer_link = None,
                answer_link = answer,
                changed_by = request.user,
            )
            new.save()
            success_message = _('Step has been added!')
            messages.success(request, success_message)
            return redirect('ah-answer-update', pk)
    else:
        form = StepUpdateForm()

    title2 = tr.pgettext('ah_answer_step_create-title', 'create-step')
    context = {
        'form': form,
        'title': title2,
        'customer': customer,
        'object': answer,
        'update_url': 'ah-answer-update',
    }
    return render(request, 'auction_house/ah_step_new.html', context)
