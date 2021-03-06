# Generated by Django 2.2.6 on 2020-01-21 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('integ', '0002_auto_20200121_1017'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_key', models.CharField(blank=True, default='type', help_text='Type key', max_length=20, null=True, verbose_name='Type key')),
            ],
            options={
                'verbose_name_plural': 'Document type',
                'verbose_name': 'Document type',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(blank=True, help_text='Name of the document.', max_length=100, null=True, verbose_name='Document name')),
                ('doc_description', models.TextField(blank=True, help_text='Description of the document.', null=True, verbose_name='Document description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='doc_repository', verbose_name='File')),
                ('thumbnail', models.ImageField(blank=True, editable=False, null=True, upload_to='doc_thumbs')),
                ('created_by', models.ForeignKey(blank=True, help_text='Link to creator', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_documents', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('open_id', models.ForeignKey(blank=True, help_text='Document Connection Key.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_docs', to='integ.OpenId', verbose_name='DCK')),
                ('type', models.ForeignKey(help_text='Document type', on_delete=django.db.models.deletion.CASCADE, related_name='my_docs', to='doc_repo.DocType', verbose_name='Type')),
            ],
            options={
                'verbose_name_plural': 'Documents',
                'verbose_name': 'Document',
            },
        ),
        migrations.CreateModel(
            name='DocTypeTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German'), ('cs', 'Czech')], max_length=15, verbose_name='language')),
                ('type_name', models.CharField(blank=True, help_text='Display name of document type.', max_length=50, null=True, verbose_name='Type name')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='doc_repo.DocType', verbose_name='doctype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
