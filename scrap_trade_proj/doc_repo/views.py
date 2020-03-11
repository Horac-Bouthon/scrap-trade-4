from django.shortcuts import render, redirect, get_object_or_404
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
    
    can_modify = user_can_modify_open_id(oid, request.user)
    od = get_owner_desc(oid, can_modify)
    document_list = get_docs_by_open_id(oid)
    
    context = {
        'docs': document_list,
        'oid': str(oid),
        'modify': can_modify,
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
    if can_modify:
        context['content_header']['button_list'].append({
            'text': _("Add Document"),
            'href': reverse('doc-repo-dokument-create',
                            kwargs={'oid': oid}),
            'icon': 'plus',
        })


    return render(request, 'doc_repo/doc_repo_doc_list.html', context)


@login_required()
@user_can_modify_owner_obj
def doc_repo_document_create(request, oid):
    
    oid_uuid = uuid.UUID(str(oid))
    obj_oid = get_object_or_404(OpenId, int_id=oid_uuid)
    
    if request.method == 'GET':
        form = DocumentCreateForm()
        
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Add the oid to the form before saving
            instance = form.save(commit=False)
            instance.open_id = obj_oid
            instance.save()
            
            success_message = _('Document has been added!')
            messages.success(request, success_message)
            return redirect('doc-repo-dokument-list', oid)

    context = {
        'form': form,
        'oid': oid,  # For cancel button
        'page_type': 'add',  # For submit button
        'content_header': {
            'title': _("Add document"), 
            'desc': _("Add a document to an object")  # @todo; Do we have a way to know what are we adding the document to?? Can we pass that in a GET attribute so the user knows?
        }        
    }
    return render(request, 'doc_repo/doc_repo_doc_form.html', context)


@login_required()
@user_can_modify_owner_obj
def doc_repo_document_modify(request, pk):
    
    doc = get_object_or_404(Document, id=pk)
    oid = str(doc.open_id.int_id)
    
    
    if request.method == 'GET':
        form = DocumentUpdateForm(instance=doc)
        
    if request.method == 'POST':
        form = DocumentUpdateForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, _('Document has been updated!'))
            return redirect('doc-repo-dokument-list', oid)

    context = {
        'form': form,
        'oid': oid,  # For cancel button
        'page_type': 'edit',  # For submit button
        'content_header': {
            'title': _("Modify the document's descriptions"),
        }
        
    }
    return render(request, 'doc_repo/doc_repo_doc_form.html', context)
