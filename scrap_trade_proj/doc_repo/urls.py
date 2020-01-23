from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as doc_views
from . views import (
    DocumentDeleteView,
)


urlpatterns = [
    path('list/<str:oid>', doc_views.doc_repo_document_list, name='doc-repo-dokument-list'),
    path('create/<str:oid>', doc_views.doc_repo_document_create, name='doc-repo-dokument-create'),
    path('modify/<int:pk>', doc_views.doc_repo_document_modify, name='doc-repo-dokument-modify'),
    path('delete/<int:pk>', DocumentDeleteView.as_view(), name='doc-repo-dokument-delete'),

]
