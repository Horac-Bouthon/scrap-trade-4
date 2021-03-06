# Generated by Django 2.2.6 on 2019-11-22 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahoffer',
            name='changed_by',
            field=models.ForeignKey(blank=True, help_text='Link to user made last change', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_changed_offers', to=settings.AUTH_USER_MODEL, verbose_name='Last change'),
        ),
    ]
