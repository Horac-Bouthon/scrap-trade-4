from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
import uuid
from . decorators import user_can_modify_owner_obj,user_can_access_owner_obj
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .models import (
    Document,
    DocType,
)
from doc_repo.modules.doc_repo_mod import OwnerDescription
from customers.models import (
    Customer,
)
from project_main.models import Project
from integ.models import (
    OpenId,
)

from integ.modules.integ_modules import (
    user_can_modify_open_id,
    user_can_acces_open_id,
    get_owner_desc,
    get_docs_by_open_id,
)

from .forms import (
    DocumentCreateForm,
    DocumentUpdateForm,
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

# Create your views here.

class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document

    def delete(self, *args, **kwargs):
        object = self.get_object()
        self.oid = str(object.open_id.int_id)
        super().delete(*args, **kwargs)
        return redirect('doc-repo-dokument-list', self.oid)

    def get_success_url(self):
        return reverse_lazy('doc-repo-dokument-list',  kwargs={'oid': self.oid})

    def test_func(self):
        object = self.get_object()
        return user_can_modify_open_id(str(object.open_id.int_id), self.request.user)


@login_required()
@user_can_access_owner_obj
def doc_repo_document_list(request, oid):
    project = Project.objects.all().first()
    modify = user_can_modify_open_id(oid, request.user)
    od = get_owner_desc(oid, modify)
    context = {
        'project': project,
        'docs': get_docs_by_open_id(oid),
        'oid': str(oid),
        'modify': modify,
        'od': od,
    }
    context['content_header'] = {
        'title': od.desc,
        'desc': _("Document management"),
    }
    context['content_header']['button_list'] = [{
        'text': _("Back"),
        'href': request.build_absolute_uri(od.url_command),
        'icon': 'arrow-left', 'type': 'secondary',
    }]
    if modify:
        new_dic = {
            'text': _("Add Document"),
            'href': reverse('doc-repo-dokument-create',
                            kwargs={'oid': oid}),
            'icon': 'plus',
        }
        context['content_header']['button_list'].append(new_dic)


    return render(request, 'doc_repo/doc_repo_doc_list.html', context)


"""
        context['content_header'] = {
            'title': customer.customer_name + ' | ' + _('Edit'),
            'desc': _("Edit customer details"),
            'image': { 'src': customer.customer_logo.url,
                       'alt': _('Customer logo') },
        }
        if test_poweruser(self.request.user):
            context['content_header']['button_list'] = [{
                'text': _("Delete Customer"),
                'href': reverse('project-customer-delete',
                                kwargs={'pk': customer.pk}),
                'icon': 'trash-2', 'type': 'danger',
            }]
        new_dic = {
            'text': _("Documents"),
            'href': reverse('doc-repo-dokument-list',
                            kwargs={'oid': oid}),
            'icon': 'eye',
        }
        if 'button_list' in context['content_header']:
            context['content_header']['button_list'].append(new_dic)
        else:
            context['content_header']['button_list'] = [new_dic,]
"""


@login_required()
@user_can_modify_owner_obj
def doc_repo_document_create(request, oid):
    proj = Project.objects.all().first()
    oid_uuid = uuid.UUID(str(oid))
    obj_oid = OpenId.objects.get(int_id = oid_uuid)
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.open_id = obj_oid
            instance.save()
            success_message = _('Document has been added!')
            messages.success(request, success_message)
            return redirect('doc-repo-dokument-list', oid)
    else:
        form = DocumentCreateForm()

    title2 = tr.pgettext('doc_repo_document_create-title', 'create-document')
    context = {
        'form': form,
        'title': title2,
        'project': proj,
        'oid': oid,
    }
    return render(request, 'doc_repo/doc_repo_doc_form.html', context)

@login_required()
@user_can_modify_owner_obj
def doc_repo_document_modify(request, pk):
    proj = Project.objects.all().first()
    doc = Document.objects.get(id = pk)
    oid = str(doc.open_id.int_id)
    if request.method == 'POST':
        form = DocumentUpdateForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            success_message = _('Document has been updated!')
            messages.success(request, success_message)
            return redirect('doc-repo-dokument-list', oid)
    else:
        form = DocumentUpdateForm(instance=doc)

    title2 = tr.pgettext('doc_repo_document_modify-title', 'update-document')
    context = {
        'form': form,
        'title': title2,
        'project': proj,
        'oid': oid,
    }
    return render(request, 'doc_repo/doc_repo_doc_form.html', context)
