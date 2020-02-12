from django import forms
from django.utils import translation as tr
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .models import (
    Document,
    DocType,
)

class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'file', 'type', 
            'doc_name', 'doc_description'
        ]


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_name', 'doc_description']
