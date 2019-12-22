from django.db import models
from PIL import Image
import os

from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from translatable.models import TranslatableModel, get_translation_model

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=50, verbose_name=_('Project name'),
            help_text=_("Project name"))
    project_description =  models.TextField(
        verbose_name=_('Project description'),
        help_text=_("Text to describe project."),
        null=True,
        blank=True,
        unique=False,
    )
    project_background = models.ImageField(
        default="default-project-background.jpg",
        upload_to='project_main',
        verbose_name=tr.pgettext_lazy('Project image', 'Background'),
        help_text=_('Image to fill Project web page background')
    )
    project_logo = models.ImageField(
        default="default-project-logo.png",
        upload_to='project_main',
        verbose_name=tr.pgettext_lazy('Project image', 'Logo'),
        help_text=_('Project logo')
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('Project definition', 'Project')
        verbose_name_plural = tr.pgettext_lazy('Project definition', 'Projects')


    def get_page_sequence(self):
        ret_val = self.staticpage_set.all().filter(sequence__gt = 0).order_by('sequence')
        return ret_val

    def __str__(self):
        return self.project_name

class StaticPage(TranslatableModel):
    page_code =  models.CharField(
        max_length=50, verbose_name=_('Page identity'),
        help_text=_("Identifikation of page"),
    )
    sequence = models.IntegerField(
        verbose_name=_('Sequence number'),
        help_text=_("Page order in the menu"),
        default = 0,
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('StaticPage definition', 'Project'),
        help_text=tr.pgettext_lazy('StaticPage definition','Link to Project'),
        null=True, blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('StaticPage definition', 'Static page')
        verbose_name_plural = tr.pgettext_lazy('StaticPage definition', 'Static pages')

    def __str__(self):
        return self.page_code

    def act_name(self):
        lang = tr.get_language()
        return self.translated('page_name', default=None, language=lang, fallback=True)

    def act_title(self):
        lang = tr.get_language()
        return self.translated('page_title', default=None, language=lang, fallback=True)

    def act_body(self):
        lang = tr.get_language()
        return self.translated('page_body', default=None, language=lang, fallback=True)



class StaticPageTranslation(get_translation_model(StaticPage, "staticpage")):
    page_name =  models.CharField(
        max_length=50, verbose_name=_('Page name'),
        help_text=_("Static page name"),
        null=True,
        blank=True,
    )
    page_title =  models.TextField(
        verbose_name=_('Page title'),
        help_text=_("Static page title."),
        null=True,
        blank=True,
    )
    page_body =  models.TextField(
        verbose_name=_('Page body'),
        help_text=_("Static page text."),
        null=True,
        blank=True,
    )
