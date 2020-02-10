from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .modules.auction import (
    resurect_auction,
    set_auction,
    customer_offer_create,
    offer_add_state,
    filter_by_state,
    customer_answer_create,
    answer_add_state,
    get_waiting_offers,
    get_auction_list_control_obj,
    ntf_send_from_view,
)

from state_wf.models import (
    StepState,
)


from customers.permissions import (
    test_poweruser, Poweruser, poweruser,
    test_user_belong_customer, UserBelongCustomer, user_belong_customer,
)
from .permissions import (
    test_user_belong_offer, UserBelongOffer, user_belong_offer,
    test_user_belong_answer, UserBelongAnswer, user_belong_answer,
)
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

class AhOfferListView(Poweruser, ListView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_list.html'
    context_object_name = 'offers'
    ordering = ['-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_header'] = {
            'title': _('Offer list'),
            'desc': _('A list of all offers in the application.'),
        }
        return context

class AhOfferListForAcceptView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_list.html'
    context_object_name = 'offers'
    ordering = ['-pk']
    permission_required = 'customers.is_poweruser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_header'] = {
            'title': _('Offers waiting for approval'),
            'desc': _('A list of offers waiting for approval in the application.'),
        }
        return context

    def get_queryset(self):
        return filter_by_state(AhOffer.objects.all(), 'offer_waiting_accept').order_by('-pk')


class AhOfferDetailView(UserBelongOffer, DetailView):
    model = AhOffer

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        offer = kwargs.get('object')

        offer.refresh_total_price()  # @todo; Pricey redundant call!

        state_key = offer.actual_state.state_key

        context.update({
            'my_answers': filter_by_state(
                offer.answers, 'answer_confirmed'
            ).order_by('-total_price')[:5],
            'answers_total': filter_by_state(
                offer.answers, 'answer_confirmed'
            ).count(),

            'bound_answers': offer.answers.filter(is_bound = True),

            'state': state_key.replace('offer_', ''),  # Trim for readability
        })

        button_list = [
            {
                'text': _("Auction"),
                'href': reverse('ah-customer-auction',
                                kwargs={'pk': offer.owner.pk}),
                'icon': 'arrow-left',
                'type': 'secondary'
            }, {
                'text': _("Documents"),
                'href': reverse('doc-repo-dokument-list',
                                kwargs={'oid': offer.open_id.int_id}),
                'icon': 'file-text',
            }
        ]
        if state_key in ['offer_new','offer_ready_to_close']:
            button_list.append({
                'text': _("Edit offer"),
                'href': reverse('ah-offer-customer-update',
                                kwargs={'pk': offer.pk}),
                'icon': 'edit-3',
            })
        if test_poweruser(self.request.user):
            button_list.append({
                'text': _("Edit offer"),
                'href': reverse('ah-offer-update',
                                kwargs={'pk': offer.pk}),
                'icon': 'edit-3',
                'type': 'poweruser',
            })
        if offer.auction_url != "":
            button_list.append({
                'text': _("Online auction"),
                'href': offer.auction_url,
                'icon': 'airplay',
                #'type': 'poweruser',
            })
        context['content_header'] = {
            'title': offer.description + ' | ' + _("Offer"),
            'desc': _("Offer detail view."),
            'button_list': button_list
        }

        return context


class AhOfferInfoView(LoginRequiredMixin, DetailView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_info.html'


class AhOfferUpdateView(Poweruser, UpdateView):
    model = AhOffer
    fields = ['description', 'delivery_date', 'auction_date',
        'minimal_total_price', 'auction_url', 'auction_start',
        'auction_end', 'offered_to',
    ]


class AhOfferCustomerUpdateView(UserBelongOffer, UpdateView):
    model = AhOffer
    fields = [
        'description', 'delivery_date', 'auction_date',
    ]
    template_name = 'auction_house/ahoffer_customer_form.html'


class AhOfferDeletelView(Poweruser, DeleteView):
    model = AhOffer
    success_url = reverse_lazy('ah-offer-list')


#--------------------------------


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


class AhDeletelOfferLine(UserPassesTestMixin, DeleteView):
    model = AhOfferLine

    def delete(self, *args, **kwargs):
        self.offer_pk = self.get_object().offer.id
        super().delete(*args, **kwargs)
        return redirect('ah-offer-detail', self.object.offer.pk)

    def get_success_url(self):
        return reverse_lazy('ah-offer-detail',  kwargs={'pk': self.offer_pk})

    def test_func(self):
        offer = self.get_object().offer
        return test_user_belong_offer(request.user, offer)


#--------------------------------

class AhMatClassDetailView(LoginRequiredMixin, DetailView):
    model = AhMatClass

#-------------------------------- ah_customer_auction
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
                'text': _("Edit customer info"),  # @todo; Add permission for customer info edit button
                'href': reverse('project-customer-detail',
                                kwargs={'pk': customer.pk}),
                'icon': 'edit-3',
            }
        ]
    }

    return render(request, 'auction_house/customer_auction.html', context)



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


from django.shortcuts import get_object_or_404

@user_belong_customer
def ah_customer_offers_by_state_key(request, pk, sk):

    customer = get_object_or_404(Customer, id=pk)
    selected_state = get_object_or_404(StepState, state_key = sk)
    filtered_offers = filter_by_state(customer.owned_offers, sk).order_by('-pk')

    translated_state_key = selected_state.get_state_name_plural()

    context = {
        'offer_list': filtered_offers,

        'content_header': {
            'title': "%s (%s)" % (translated_state_key,
                                  customer.customer_name),
            'desc': _("List of offers"),
            'image': { 'src': customer.customer_logo.url,
                       'alt': _('Customer logo') },
            'button_list': [{
                'text': _('Auction'),
                'href': reverse('ah-customer-auction',
                                kwargs={'pk': customer.pk}),
                'icon': 'arrow-left',
                'type': 'secondary',
            }],
        },
    }
    return render(request, 'auction_house/customer_offer_list.html', context)


@user_belong_customer
def ah_offers_change_state(request, pk, pk2, pk3):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()
    set_state = StepState.objects.get(id=pk3)

    if request.method == 'POST':
        offer_add_state(offer, set_state, request.user)
        if set_state.state_key == 'offer_confirmed':
            # TODO: zmenit na skutecnou adresu online aukce
            offer.auction_url = request.build_absolute_uri(reverse('ah-offer-detail', kwargs={'pk': offer.id}))
            offer.save()
        if set_state.state_key == 'offer_canceled':
            state_send = StepState.objects.get(state_key = 'answer_canceled')
            for answer in offer.answers.all():
                answer_add_state(answer, state_send, request.user)

        if set_state.send_ntf:
            ntf_send_from_view(
                request=request,
                state=set_state,
                place='auction_house.view - ah_offers_change_state()',
                item=offer,
            )

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
                ntf_send_from_view(
                    request=request,
                    state=state_send,
                    place='auction_house.view - ah_answer_change_state() - answer_accepted',
                    item=answer.ah_offer,
                )
        if set_state.state_key == 'answer_closed':
            state_send = StepState.objects.get(state_key = 'offer_ready_to_close')
            offer_add_state(answer.ah_offer, state_send, request.user)
            if state_send.send_ntf:
                ntf_send_from_view(
                    request=request,
                    state=state_send,
                    place='auction_house.view - ah_answer_change_state() - answer_closed',
                    item=answer.ah_offer,
                )
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
class AhAnswerListView(Poweruser, ListView):
    model = AhAnswer
    template_name = 'auction_house/ahanswer_list.html'
    context_object_name = 'answers'
    ordering = ['-pk']


class AhAnswerDetailView(UserBelongAnswer, DetailView):
    model = AhAnswer
    template_name = 'auction_house/ahanswer_detail.html'

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


class AhAnswerUpdateView(Poweruser, UpdateView):
    model = AhAnswer
    fields = [
        'description',
        'owner',
        'ah_offer',
        'is_bound',
        'auction_url',
    ]



class AhAnswerCustomerUpdateView(UserBelongAnswer, UpdateView):
    model = AhAnswer
    fields = [
        'description',
    ]
    template_name = 'auction_house/ahanswer_customer_form.html'


class AhAnswerDeletelView(Poweruser, DeleteView):
    model = AhAnswer
    success_url = reverse_lazy('ah-answer-list')



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



@user_belong_customer
def ah_customer_answer_by_state_key(request, pk, sk):
    customer = Customer.objects.filter(id = pk).first()
    title2 = tr.pgettext('ah_customer_answer_by_state_key-title', 'answers-by-state')
    selected_state = StepState.objects.filter(state_key = sk).first()
    context = {
        'title': title2,
        'selection': selected_state.get_state_name_plural(),
        'customer': customer,
        'answer_list': filter_by_state(customer.owned_answers, sk).order_by('-pk'),
    }
    return render(request, 'auction_house/customer_answer_list.html', context)


@user_belong_customer
def ah_customer_answer_create(request, pk, pk2):
    customer = Customer.objects.filter(id = pk).first()
    offer = AhOffer.objects.filter(id = pk2).first()
    user = request.user

    if request.method == 'POST':
        form = AhAnwserCreateForm(request.POST)
        if form.is_valid():
            customer_answer_create(request, customer, offer, user, form.cleaned_data)
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
            #todo; Aggregates :: Sum()
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


@poweruser
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


@poweruser
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



## REALTIME AUCTION
import django.utils.timezone as django_timezone

@login_required
def realtime_auction(request):

    offer = AhOffer.objects.first()  #mock

    context = {
        'offer': offer, 'object': offer,
        'content_header': {
            'title': offer.description,
            'desc': _("Realtime auction"),
            'image': { 'src': offer.owner.customer_logo.url,
                       'alt': _('Customer logo') },
        },
    }

    mock = {  #mock
        'arrival': 'ok',
        'start_datetime': django_timezone.now(),
    }
    context.update(mock)

    return render(request, 'auction_house/realtime_auction.html', context)
