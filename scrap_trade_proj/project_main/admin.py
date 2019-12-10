from django.contrib import admin

from project_main.models import (
    Project,
    StaticPage,
    StaticPageTranslation,
)

from django.utils.translation import gettext_lazy as _
from django.conf import settings


class StaticPageTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
    model = StaticPageTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class StaticPageAdmin(admin.ModelAdmin):
    inlines = [StaticPageTranslationInlineAdmin,]


# Register your models here.
admin.site.register(Project)
admin.site.register(StaticPage, StaticPageAdmin)
