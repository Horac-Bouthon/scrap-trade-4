# Generated by Django 2.2.6 on 2020-01-21 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('integ', '0002_auto_20200121_1017'),
        ('auction_house', '0027_ahoffer_open_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ahofferline',
            name='open_id',
            field=models.ForeignKey(blank=True, help_text='Link to integration key', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_offer_lines', to='integ.OpenId', verbose_name='Open id'),
        ),
    ]