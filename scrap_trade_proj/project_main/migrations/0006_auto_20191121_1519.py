# Generated by Django 2.2.6 on 2019-11-21 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_main', '0005_staticpagetranslation_page_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staticpage',
            old_name='idetity',
            new_name='page_code',
        ),
    ]
