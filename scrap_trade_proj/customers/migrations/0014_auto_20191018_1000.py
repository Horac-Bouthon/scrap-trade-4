# Generated by Django 2.2.6 on 2019-10-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_basicphonecategory_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicphonecategory',
            name='type',
        ),
        migrations.AddField(
            model_name='basicphonecategory',
            name='phohe_type',
            field=models.CharField(blank=True, default='phone', help_text='Phone category type', max_length=50, null=True, verbose_name='Type'),
        ),
    ]
