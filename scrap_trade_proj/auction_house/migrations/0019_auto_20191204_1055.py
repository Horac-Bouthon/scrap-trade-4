# Generated by Django 2.2.6 on 2019-12-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0018_auto_20191204_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahoffer',
            name='auction_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ahoffer',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
