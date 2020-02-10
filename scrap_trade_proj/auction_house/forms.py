from django import forms
from django.utils import translation as tr
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .models import (
    AhOffer,
    AhOfferLine,
    AhAnswer,
    AhAnswerLine,
)
from state_wf.models import (
    Step,
    StepState,
)


class AhOfferLineUpdateForm(forms.ModelForm):
    class Meta:
        model = AhOfferLine
        fields = ['description', 'amount', 'mat_class', 'minimal_ppu']


class AhOfferUpdateForm(forms.ModelForm):
    
    auction_date = forms.DateField(
        label=_('Auction date:'), 
        initial=datetime.now(), 
        widget=forms.SelectDateWidget)
    
    delivery_date = forms.DateField(
        label=_('Delivery date:'), 
        initial=datetime.now(), 
        widget=forms.SelectDateWidget)
    
    class Meta:
        model = AhOffer
        fields = ['description', ]


class AhAnwserCreateForm(forms.ModelForm):
    class Meta:
        model = AhAnswer
        fields = ['description']


class AhAnwserLinePpuUpdateForm(forms.ModelForm):
    class Meta:
        model = AhAnswerLine
        fields = ['ppu']


class AhAnwserLineTotalUpdateForm(forms.ModelForm):
    class Meta:
        model = AhAnswerLine
        fields = ['total_price']

class StepUpdateForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['state', ]
