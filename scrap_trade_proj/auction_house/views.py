from django.shortcuts import render, redirect, get_object_or_404
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
    OnlineBestBet,
    get_online_info_context,
    get_online_context,
    answer_update_ppu,
)

from state_wf.models import (
    StepState,
    Step,
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


def get_state(state_key):  #util
    assert isinstance(state_key, str), "state_key must be a string"
    return get_object_or_404(StepState, state_key=state_key)


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

class AhOfferListForAcceptView(Poweruser, ListView):
    model = AhOffer
    template_name = 'auction_house/ahoffer_list.html'
    context_object_name = 'offers'
    ordering = ['-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_header'] = {
            'title': _('Offers waiting for approval'),
            'desc': _(('A list of offers waiting for approval in the application.')),
        }
        return context

    def get_queryset(self):
        return filter_by_state(
            AhOffer.objects.all(), 'offer_waiting_accept').order_by('-pk')


class AhOfferDetailView(UserBelongOffer, DetailView):
    model = AhOffer

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        offer = kwargs.get('object')
        state_key = offer.actual_state.state_key

        offer.refresh_total_price()  # @todo; Pricey redundant call!

        context.update({
            'offer': offer,
            'customer': offer.owner,
        })

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
        
        edit_button = {
            'text': _("Edit offer"),
            'icon': 'edit-3',
        }
        if state_key in ['offer_new','offer_ready_to_close']:
            edit_button.update({
                'href': reverse('ah-offer-customer-update', args=[offer.pk])
            })
        elif test_poweruser(self.request.user):
            edit_button.update({
                'href': reverse('ah-offer-update', args=[offer.pk])
                'type': 'poweruser',
            })
        button_list.append(edit_button)

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

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        offer = kwargs.get('object')
        context['customer'] = offer.owner

        return context


class AhOfferUpdateView(Poweruser, UpdateView):
    model = AhOffer
    fields = ['description', 'auction_date', 'delivery_date',
        'minimal_total_price', 'auction_url', 'auction_start',
        'auction_end', 'offered_to',
    ]

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        offer = context['object']
        context.update({
            'customer': offer.owner,
            'poweruser': True,
            'content_header': {
                'title': ' | '.join([_("Edit offer"),
                                     offer.description]),
                'desc': _("Edit offer as a poweruser."),
                'button_list': [{
                    'text': 'Offer',
                    'icon': 'arrow-left',
                    'type': 'secondary',
                    'href': reverse('ah-offer-detail', args=[offer.pk]),
                }],
            },
        })
        return context



class AhOfferCustomerUpdateView(UserBelongOffer, UpdateView):
    model = AhOffer
    fields = [
        'description',
        'auction_date',
        'delivery_date',
    ]
    template_name = 'auction_house/ahoffer_customer_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)

        offer = context['object']
        context['customer'] = offer.owner

        context['content_header'] = {
            'title': ' | '.join([offer.description,
                                 _("Edit offer")]),
            'desc': _("Modify the offer's data."),
            'button_list': [{
                'text': 'Offer',
                'icon': 'arrow-left',
                'type': 'secondary',
                'href': reverse('ah-offer-detail', args=[offer.pk]),
            }],
        }

        return context


class AhOfferDeletelView(Poweruser, DeleteView):
    model = AhOffer
    success_url = reverse_lazy('ah-offer-list')


#--------------------------------


@user_belong_offer
def ah_offer_line_update(request, pk, pk2):

    offer = get_object_or_404(AhOffer, id = pk)
    offer_line = get_object_or_404(AhOfferLine, id = pk2)

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

    context = {
        'form': form,
        'offer': offer,
        'customer': offer.owner,
        'content_header': {
            'title': " | ".join([offer.description, _('Edit line')]),
            'desc': _('Edit a specific line in the offer.')
        },
        'page_type': 'update',  # Same template is used for update and create
    }
    return render(request, 'auction_house/offer_line_form.html', context)


@user_belong_offer
def ah_offer_line_create(request, pk):

    offer = get_object_or_404(AhOffer, id = pk)

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

    context = {
        'form': form,
        'offer': offer,
        'customer': offer.owner,
        'content_header': {
            'title': ' | '.join([offer.description, _('Add a line')]),
            'desc': _("Add a new product for offer."),
            'button_list': [{
                'text': 'Offer',
                'icon': 'arrow-left',
                'type': 'secondary',
                'href': reverse('ah-offer-detail', args=[offer.pk]),
            }],
        },
        'page_type': 'create',  # Same template is used for update and create
    }
    return render(request, 'auction_house/offer_line_form.html', context)


class AhDeletelOfferLine(UserPassesTestMixin, DeleteView):
    model = AhOfferLine

    def delete(self, *args, **kwargs):
        self.offer_pk = self.get_object().offer.id
        super().delete(*args, **kwargs)
        return redirect('ah-offer-detail', self.object.offer.pk)

    def get_success_url(self):
        return reverse_lazy('ah-offer-detail',  args=[self.offer_pk])

    def test_func(self):
        offer = self.get_object().offer
        return test_user_belong_offer(request.user, offer)


#--------------------------------

class AhMatClassDetailView(LoginRequiredMixin, DetailView):
    model = AhMatClass

#-------------------------------- ah_customer_auction
@user_belong_customer
def ah_customer_auction(request, pk):

    customer = get_object_or_404(Customer, id = pk)

    auc_obj = get_auction_list_control_obj(
        customer, customer.owned_offers, customer.owned_answers)

    context = {
        'customer': customer,
        'auc_obj': auc_obj,
    }

    context['content_header'] = {
        'title': ' | '.join([customer.customer_name, _('Auction')]),
        'desc': _('Auction homepage'),

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

    customer = get_object_or_404(Customer, id = pk)

    if request.method == 'POST':
        form = AhOfferUpdateForm(request.POST)
        if form.is_valid():
            customer_offer_create(
                customer = customer,
                user = request.user,
                data = form.cleaned_data
            )
            messages.success(request,
                             _('Your offer has been added!'))
            return redirect('ah-customer-auction', pk)
    else:
        form = AhOfferUpdateForm()

    context = {
        'content_header': {
            'title': _("New offer"),
            'desc': _("Create a new auction offer")
        },
        'form': form,
        'customer': customer,
    }
    return render(request, 'auction_house/ahoffer_customer_new.html', context)


@user_belong_customer
def ah_customer_offers_by_state_key(request, pk, sk):

    customer = get_object_or_404(Customer, id=pk)
    selected_state = get_state(sk)
    filtered_offers = filter_by_state(customer.owned_offers, sk).order_by('-pk')

    translated_state_key = selected_state.get_state_name_plural()

    context = {
        'offer_list': filtered_offers,

        'customer': customer,
        'content_header': {
            'title': "%s (%s)" % (translated_state_key,
                                  customer.customer_name),
            'desc': _("List of offers"),
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

    customer = get_object_or_404(Customer, id = pk)
    offer = get_object_or_404(AhOffer, id = pk2)
    set_state = StepState.objects.get(id=pk3)

    # @todo; Is there any permission checking offer state changes?

    if request.method == 'GET':
        pass  # Don't do anything, just ask for accept -> POST

    elif request.method == 'POST':
        offer_add_state(offer, set_state, request.user)

        if set_state.state_key == 'offer_confirmed':
            offer.auction_url = request.build_absolute_uri(reverse('realtime-auction-info', kwargs={'pk': offer.id}))
            offer.save()
        elif set_state.state_key == 'offer_canceled':
            state_send = get_state('answer_canceled')
            my_answers = filter_by_state(offer.answers, 'answer_confirmed')
            for answer in my_answers.all():
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

    context = {
        'customer': customer,
        'offer': offer,
        'state': set_state,
    }
    return render(request, 'auction_house/ahoffer_change_state.html', context)


@user_belong_customer
def ah_answer_change_state(request, pk, pk2, pk3):

    customer = get_object_or_404(Customer, id = pk)
    answer = get_object_or_404(AhAnswer, id = pk2)
    set_state = StepState.objects.get(id=pk3)

    if request.method == 'GET':
        pass  # Don't do anything, just ask for accept -> POST

    elif request.method == 'POST':
        answer_add_state(answer, set_state, request.user)
        if set_state.state_key == 'answer_accepted':
            state_send = get_state('offer_accepted')
            offer_add_state(answer.ah_offer, state_send, request.user)
            if state_send.send_ntf:
                ntf_send_from_view(
                    request=request,
                    state=state_send,
                    place='auction_house.view - ah_answer_change_state() - answer_accepted',
                    item=answer.ah_offer,
                )
        elif set_state.state_key == 'answer_closed':
            state_send = get_state('offer_ready_to_close')
            offer_add_state(answer.ah_offer, state_send, request.user)
            if state_send.send_ntf:
                ntf_send_from_view(
                    request=request,
                    state=state_send,
                    place='auction_house.view - ah_answer_change_state() - answer_closed',
                    item=answer.ah_offer,
                )
        elif set_state.state_key == 'answer_canceled' and answer.is_bound:
            resurect_auction(answer.ah_offer)
            set_auction(request, answer.ah_offer)

        success_message = _('Your answer has change the state!')
        messages.success(request, success_message)
        return redirect('ah-customer-auction', pk)

    context = {
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

        answer = kwargs.get('object')
        answer.refresh_total_price()

        state_key = answer.actual_state.state_key

        context.update({
            'answer': answer,
            'customer': answer.owner,  # @todo; Should we show logo of answer owner or the offer owner??
            'offer': answer.ah_offer,
            'state': state_key.replace('answer_', ''),
        })

        button_list = [
            {
                'text': _("Auction"),
                'href': reverse('ah-customer-auction',
                                kwargs={'pk': answer.owner.pk}),
                'icon': 'arrow-left',
                'type': 'secondary'
            }, {
                'text': _("Documents"),
                'href': reverse('doc-repo-dokument-list',
                                kwargs={'oid': answer.open_id.int_id}),
                'icon': 'file-text',
            }
        ]

        if test_poweruser(self.request.user):
            button_list.append({
                'text': _("Edit answer"),
                'href': reverse('ah-answer-update',
                                kwargs={'pk': answer.pk}),
                'icon': 'edit-3',
                'type': 'poweruser',
            })
        elif state_key in [
                'answer_new', 'answer_successful', 'answer_accepted']:
            button_list.append({
                'text': _("Edit description"),
                'href': reverse('ah-answer-customer-update',
                                kwargs={'pk': answer.pk}),
                'icon': 'edit-3',
            })

        if answer.auction_url != "":
            button_list.append({
                'href': answer.auction_url,
                'text': _("Online auction"),
                'icon': 'airplay',
                #'type': 'poweruser',
            })
        context['content_header'] = {
            'title': answer.description + ' | ' + _("Answer"),
            'desc': '%s "%s"' % (_("Detailed view of an answer to:"),
                               answer.ah_offer.description),
            'button_list': button_list
        }

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
    customer = get_object_or_404(Customer, id = pk)
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

    customer = get_object_or_404(Customer, id = pk)
    translated_state_key = get_state(sk).get_state_name_plural()
    filtered_answers = filter_by_state(customer.owned_answers, sk).order_by('-pk')

    context = {
        'answer_list': filtered_answers,

        'customer': customer,
        'content_header': {
            'title': "%s (%s)" % (translated_state_key,
                                customer.customer_name),
            'desc': _("List of answers"),
            'button_list': [{
                'text': _('Auction'),
                'href': reverse('ah-customer-auction',
                                kwargs={'pk': customer.pk}),
                'icon': 'arrow-left',
                'type': 'secondary',
            }],
        }
    }
    return render(request, 'auction_house/customer_answer_list.html', context)


@user_belong_customer
def ah_customer_answer_create(request, pk, pk2):

    customer = get_object_or_404(Customer, id = pk)
    offer = get_object_or_404(AhOffer, id = pk2)
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
    context['content_header'] = {
        'title': customer.customer_name + ' | ' + _('New answer'),
        'desc': _('Create new answer'),

        'button_list': [
            {
                'text': _("Auction"),
                'href': reverse('ah-customer-auction',
                                kwargs={'pk': customer.pk}),
                'icon': 'arrow-left',
                'type': 'secondary'
            },
        ]
    }
    return render(request, 'auction_house/ahanswer_customer_new.html', context)




@user_belong_answer
def ah_answer_line_update_ppu(request, pk, pk2):

    answer = get_object_or_404(AhAnswer, id = pk)
    answer_line = get_object_or_404(AhAnswerLine, id = pk2)

    if request.method == 'POST':
        form = AhAnwserLinePpuUpdateForm(request.POST, instance=answer_line)
        if form.is_valid():
            form.save()
            answer_update_ppu(answer_line)
            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('ah-answer-detail', pk)
    else:
        form = AhAnwserLinePpuUpdateForm(instance=answer_line)

    context = {
        'ppu_form': form,
        'answer': answer,
        'min_price_ppu': answer_line.offer_line.minimal_ppu,
    }
    return render(request, 'auction_house/answer_line_form.html', context)


@user_belong_answer
def ah_answer_line_update_total(request, pk, pk2):

    answer = get_object_or_404(AhAnswer, id = pk)
    answer_line = get_object_or_404(AhAnswerLine, id = pk2)

    if request.method == 'POST':
        form = AhAnwserLineTotalUpdateForm(request.POST, instance=answer_line)
        if form.is_valid():
            form.save()

            answer_line.ppu = answer_line.total_price / answer_line.offer_line.amount
            answer_line.save()

            sum = 0
            for line in answer.my_lines.all():
                sum += line.total_price
            answer.total_price = sum
            answer.save()

            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('ah-answer-detail', pk)
    else:
        form = AhAnwserLineTotalUpdateForm(instance=answer_line)

    context = {
        'total_form': form,
        'answer': answer,
        'min_price_total': answer_line.offer_line.minimal_ppu * answer_line.offer_line.amount,
    }
    return render(request, 'auction_house/answer_line_form.html', context)


@poweruser
def ah_offer_step_create(request, pk):

    offer = get_object_or_404(AhOffer, id = pk)

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
        'customer': offer.owner,
        'object': offer,
        'update_url': 'ah-offer-update',
    }
    return render(request, 'auction_house/ah_step_new.html', context)


@poweruser
def ah_answer_step_create(request, pk):
    answer = get_object_or_404(AhAnswer, id = pk)
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

#@login_required
@user_belong_answer
def realtime_auction(request, pk2, pk):
    context = get_online_context(pk2, pk)
    return render(request, 'auction_house/realtime_auction.html', context)


@user_belong_answer
def ah_answer_online_update_ppu(request, pk, pk2):

    answer = get_object_or_404(AhAnswer, id = pk)
    answer_line = get_object_or_404(AhAnswerLine, id = pk2)

    if request.method == 'POST':
        form = AhAnwserLinePpuUpdateForm(request.POST, instance=answer_line)
        if form.is_valid():
            form.save()
            answer_update_ppu(answer_line)
            success_message = _('Your line has been updated!')
            messages.success(request, success_message)
            return redirect('realtime-auction', answer.ah_offer.pk, answer.pk)
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

@login_required
def realtime_auction_info(request, pk):
    context = get_online_info_context(pk)
    return render(request, 'auction_house/realtime_auction_info.html', context)
