from django.contrib import admin

# Register your models here.
from doc_repo.models import (
    DocType,
    DocTypeTranslation,
    Document,
)

from django.utils.translation import gettext_lazy as _
from django.conf import settings


class DocTypeTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Document type")
    verbose_name_plural = _("Document types")
    model = DocTypeTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class DocTypeAdmin(admin.ModelAdmin):
    inlines = [DocTypeTranslationInlineAdmin,]


admin.site.register(Document)
admin.site.register(DocType, DocTypeAdmin)
