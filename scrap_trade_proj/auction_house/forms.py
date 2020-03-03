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
            
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError(
                _("Amount has to be positive")
            )
        return amount
    
    def clean_minimal_ppu(self): 
        unit_price = self.cleaned_data['minimal_ppu']
        if unit_price < 0:
            raise forms.ValidationError(
                _("Unit price has to be positive or zero (= no minimum)")
            )
        return unit_price



class AhOfferUpdateForm(forms.ModelForm):
    
    auction_date = forms.DateField(
        label=_('Auction date:'), 
        initial=datetime.now
    )
    
    delivery_date = forms.DateField(
        label=_('Delivery date:'), 
        initial=datetime.now
    )
    
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
