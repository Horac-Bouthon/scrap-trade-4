# Generated by Django 2.2.6 on 2020-01-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state_wf', '0008_auto_20200106_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepstatetranslation',
            name='is_allerrt',
            field=models.BooleanField(default=False, help_text='Show button like allert. ', verbose_name='Allert button'),
        ),
        migrations.AddField(
            model_name='stepstatetranslation',
            name='state_template_cancel_button',
            field=models.CharField(blank=True, help_text='Template state cancel button text.', max_length=50, null=True, verbose_name='State template cancel button'),
        ),
        migrations.AddField(
            model_name='stepstatetranslation',
            name='state_template_title',
            field=models.CharField(blank=True, help_text='Template title text.', max_length=200, null=True, verbose_name='State template title'),
        ),
    ]
