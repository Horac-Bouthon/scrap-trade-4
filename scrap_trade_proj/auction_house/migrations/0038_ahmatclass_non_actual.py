# Generated by Django 2.2.10 on 2020-03-16 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0037_auto_20200316_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='ahmatclass',
            name='non_actual',
            field=models.BooleanField(default=False, help_text='Mark not actual materials. ', verbose_name='Not actual'),
        ),
    ]