# Generated by Django 2.2.6 on 2019-10-18 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0016_customerphone_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerphone',
            name='desctiption',
            field=models.CharField(blank=True, help_text='Phone description', max_length=255, null=True, verbose_name='Description'),
        ),
    ]
