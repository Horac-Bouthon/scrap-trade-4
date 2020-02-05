from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from project_main.models import Project

#from .forms import (
#)

from django.utils import translation as tr
from django.utils.translation import gettext as _
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
