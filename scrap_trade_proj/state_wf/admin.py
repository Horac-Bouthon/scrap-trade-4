from django.contrib import admin

from state_wf.models import (
    StepState,
    StepStateTranslation,
    Step,
)

from django.utils.translation import gettext_lazy as _
from django.conf import settings

class StepStateTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Translation")
    verbose_name_plural = _("Translations")
    model = StepStateTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1

class StepStateAdmin(admin.ModelAdmin):
    inlines = [StepStateTranslationInlineAdmin,]

# Register your models here.
admin.site.register(StepState, StepStateAdmin)
admin.site.register(Step)
