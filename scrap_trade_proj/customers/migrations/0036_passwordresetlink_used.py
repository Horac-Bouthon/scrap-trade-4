# Generated by Django 2.2.6 on 2020-01-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0035_auto_20200129_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresetlink',
            name='used',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]