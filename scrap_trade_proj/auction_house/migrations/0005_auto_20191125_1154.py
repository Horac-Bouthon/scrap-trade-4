# Generated by Django 2.2.6 on 2019-11-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0004_ahoffer_offered_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahoffer',
            name='offered_to',
            field=models.ManyToManyField(help_text='List of customers who received the offer', related_name='receive_offers', to='customers.Customer', verbose_name='Offered to'),
        ),
    ]
