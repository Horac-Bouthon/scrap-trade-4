from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid

from pdf2image import convert_from_path
from django.utils.translation import gettext_lazy as _
from django.utils import translation as tr

from translatable.models import TranslatableModel, get_translation_model

from project_main.models import Project
from integ.models import OpenId

from customers.models import (
    ProjectCustomUser,
)

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from scrap_trade_proj.settings import THUMB_SIZE
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.

class DocType(TranslatableModel):
    type_key = models.CharField(
        max_length=20,
        default="type",
        verbose_name=tr.pgettext_lazy('DocType definition', 'Type key'),
        help_text=tr.pgettext_lazy('DocType definition','Type key'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = tr.pgettext_lazy('DocType definition', 'Document type')
        verbose_name_plural = tr.pgettext_lazy('DocType definition', 'Document type')

    def __str__(self):
        return self.get_type_name()

    def get_type_name(self):
        lang = tr.get_language()
        return self.translated('type_name', default=None, language=lang, fallback=True)


class DocTypeTranslation(get_translation_model(DocType, "doctype")):
    type_name = models.CharField(
        verbose_name=_('Type name'),
        help_text=_("Display name of document type."),
        max_length=50,
        null=True,
        blank=True,
        unique=False
    )


class Document(models.Model):
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=_('Open ID'),
        help_text=_("Document Connection Key."),
        related_name='my_docs',
        null=True, blank=True,
    )
    doc_name = models.CharField(
        verbose_name=_('Document name'),
        help_text=_("Name of the document."),
        max_length=100,
        null=True,
        blank=True,
        unique=False,
        )
    doc_description =  models.TextField(
        verbose_name=_('Document description'),
        help_text=_("Description of the document."),
        null=True,
        blank=True,
        unique=False,
    )
    type = models.ForeignKey(
        DocType,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('Document definition', 'Type'),
        help_text=tr.pgettext_lazy('Document definition','Document type'),
        related_name="my_docs",
    )
    created_by = models.ForeignKey(
        ProjectCustomUser,
        on_delete=models.SET_NULL,
        verbose_name=tr.pgettext_lazy('Document definition', 'Created by'),
        help_text=tr.pgettext_lazy('Document definition','Link to creator'),
        null=True, blank=True,
        related_name="my_documents",
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    file = models.FileField(
        upload_to='doc_repository/%Y/%m/%d/',
        verbose_name=tr.pgettext_lazy('Document file', 'File'),
        null=True,
        blank=True,
    )
    thumbnail = models.ImageField(
        upload_to='doc_thumbs/%Y/%m/%d/',
        editable=False,
        null=True,
        blank=True,
    )
    open_id = models.ForeignKey(
        OpenId,
        on_delete=models.CASCADE,
        verbose_name=tr.pgettext_lazy('UserProfile definition', 'Open id'),
        help_text=tr.pgettext_lazy('UserProfile definition','Link to integration key'),
        related_name='my_docs',
        null=True, blank=True,
    )



    class Meta:
        verbose_name = tr.pgettext_lazy('Document definition', 'Document')
        verbose_name_plural = tr.pgettext_lazy('Document definition', 'Documents')

    def __str__(self):
        return '{} {} {}'.format(self.pk,
            self.doc_name,
            self.created_at,
        )

    def is_picture(self):
        return self.type == DocType.objects.get(type_key = 'picture')

    def is_pdf(self):
        return self.type == DocType.objects.get(type_key = 'pdf')

    def is_file(self):
        return self.type == DocType.objects.get(type_key = 'file')

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super().save(*args, **kwargs)
        self.make_thumbnail()

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        if self.type == DocType.objects.get(type_key = 'picture') and self.thumbnail == None:
            return self.make_picture_thumb()
        if self.type == DocType.objects.get(type_key = 'pdf') and self.thumbnail == None:
            return self.make_pdf_thumb()
        return True

    def make_picture_thumb(self):
        try:
            image = Image.open(self.file.path)
        except:
            return False
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.file.name)
        xl = thumb_name.split('/')
        thumb_real_name = xl[-1]
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_real_name + '_thumb' + thumb_extension
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
        return True

    def make_pdf_thumb(self):
        try:
            pages = convert_from_path(self.file.path, 500)
            print('pages = {}'.format(pages))
        except:
            print('error excepted')
            return False
        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.file.name)
        xl = thumb_name.split('/')
        thumb_real_name = xl[-1]
        thumb_filename = thumb_real_name + '_thumb.jpg'
        FTYPE = 'JPEG'
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        for page in pages:
            page.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)
        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
        img = Image.open(self.thumbnail.path)
        if img.height > 100 or img.width > 100:
            img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
            img.save(self.thumbnail.path)
        return True
