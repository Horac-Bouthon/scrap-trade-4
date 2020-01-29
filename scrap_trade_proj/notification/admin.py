from django.contrib import admin
from django.conf import settings
from .models import NtfSetup, MessTemp, MessTempTranslation
from django.utils.translation import gettext_lazy as _

# Register your models here.


class MessTempTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Message template")
    verbose_name_plural = _("Message template")
    model = MessTempTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1


class MessTempAdmin(admin.ModelAdmin):
    inlines = [MessTempTranslationInlineAdmin,]


admin.site.register(MessTemp, MessTempAdmin)
admin.site.register(NtfSetup)
