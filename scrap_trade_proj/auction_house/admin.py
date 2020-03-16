from django.contrib import admin

# Register your models here.
from auction_house.models import (
    AhOffer,
    AhOfferLine,
    AhMatClass,
    AhMatClassTranslation,
    AhAnswer,
    AhAnswerLine,
    Catalog,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class AhMatClassTranslationInlineAdmin(admin.StackedInline):
    verbose_name = _("Material class")
    verbose_name_plural = _("Material class")
    model = AhMatClassTranslation
    max_num = len(settings.LANGUAGES)
    extra = 1

class AhMatClassAdmin(admin.ModelAdmin):
    inlines = [AhMatClassTranslationInlineAdmin,]


admin.site.register(AhOffer)
admin.site.register(AhOfferLine)
admin.site.register(AhMatClass, AhMatClassAdmin)
admin.site.register(AhAnswer)
admin.site.register(AhAnswerLine)
admin.site.register(Catalog)
