# Generated by Django 2.2.6 on 2019-12-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0020_auto_20191205_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahanswerline',
            name='ppu',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Price for one measurement unit', max_digits=7, verbose_name='Price per unit'),
        ),
        migrations.AlterField(
            model_name='ahanswerline',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Final price for the line', max_digits=10, verbose_name='Total price'),
        ),
    ]
