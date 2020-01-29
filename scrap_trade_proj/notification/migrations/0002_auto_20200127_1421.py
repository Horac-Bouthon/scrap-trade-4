# Generated by Django 2.2.6 on 2020-01-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ntfsetup',
            name='serve_email',
            field=models.BooleanField(default=True, help_text='Can send emails.', verbose_name='Send emails'),
        ),
        migrations.AddField(
            model_name='ntfsetup',
            name='serve_sms',
            field=models.BooleanField(default=False, help_text='Can send SMS.', verbose_name='Send SMS'),
        ),
    ]
