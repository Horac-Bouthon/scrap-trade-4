from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from project_main.models import Project

from django.utils import translation as tr
from django.utils.translation import gettext as _


def spa(request): 
    
    if request.method == 'POST':
        # Attempt at logging in
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():  # Also checks credentials!
            login(request, auth_form.get_user())
            return redirect('project-customer-home')
        else: 
            # @todo; Redirect to the proper login page where errors will be more readable
            pass 
    else:
        # Empty login form
        auth_form = AuthenticationForm()
        # Strip the autofocus, we don't want login always focused on the homepage
        auth_form.fields['username'].widget.attrs.pop("autofocus", None)
    
    project = Project.objects.first()
    static_page_sections = project.staticpage_set.all().order_by('sequence')
    
    return render(request, 'project_main/homepage_spa.html', {
        'form_login': auth_form, 
        'project': project,
        'sections': static_page_sections,
    })



def home_project(request):
    proj = Project.objects.all().first()
    stat_page = proj.staticpage_set.filter(page_code = 'project-home').first()
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user_f = form_login.get_user()
            login(request, user_f)
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
    else:
        form_login = AuthenticationForm()
    title2 = tr.pgettext('project-home-title2', 'home')
    context = {
        'form_login': form_login,
        'title': title2,
        'project': proj,
        'stat_page': stat_page,
    }
    return render(request, 'project_main/static_page.html', context)

def who_are_we(request):
    proj = Project.objects.all().first()
    stat_page = proj.staticpage_set.filter(page_code = 'who_are_we').first()
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user_f = form_login.get_user()
            login(request, user_f)
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
    else:
        form_login = AuthenticationForm()
    title2 = tr.pgettext('who_are_we-title2', 'who are we')
    context = {
        'form_login': form_login,
        'title': title2,
        'project': proj,
        'stat_page': stat_page,
    }
    return render(request, 'project_main/static_page.html', context)

def how_we_work(request):
    proj = Project.objects.all().first()
    stat_page = proj.staticpage_set.filter(page_code = 'how_we_work').first()
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user_f = form_login.get_user()
            login(request, user_f)
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
    else:
        form_login = AuthenticationForm()
    title2 = tr.pgettext('how_we_work-title2', 'how we work')
    context = {
        'form_login': form_login,
        'title': title2,
        'project': proj,
        'stat_page': stat_page,
    }
    return render(request, 'project_main/static_page.html', context)

def partners(request):
    proj = Project.objects.all().first()
    stat_page = proj.staticpage_set.filter(page_code = 'partners').first()
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user_f = form_login.get_user()
            login(request, user_f)
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
    else:
        form_login = AuthenticationForm()
    title2 = tr.pgettext('partners-title2', 'partners')
    context = {
        'form_login': form_login,
        'title': title2,
        'project': proj,
        'stat_page': stat_page,
    }
    return render(request, 'project_main/static_page.html', context)

def contacts(request):
    proj = Project.objects.all().first()
    stat_page = proj.staticpage_set.filter(page_code = 'contacts').first()
    if request.method == 'POST':
        form_login = AuthenticationForm(data=request.POST)
        if form_login.is_valid():
            user_f = form_login.get_user()
            login(request, user_f)
            if user_f.customer:
                return redirect('ah-customer-auction', user_f.customer.pk)
            return redirect('project-customer-home')
    else:
        form_login = AuthenticationForm()
    title2 = tr.pgettext('contacts-title2', 'contacts')
    context = {
        'form_login': form_login,
        'title': title2,
        'project': proj,
        'stat_page': stat_page,
    }
    return render(request, 'project_main/static_page.html', context)
