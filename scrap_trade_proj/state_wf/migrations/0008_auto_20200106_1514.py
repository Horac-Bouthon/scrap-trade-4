# Generated by Django 2.2.6 on 2020-01-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state_wf', '0007_stepstate_manual_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepstate',
            name='manual_set',
            field=models.BooleanField(default=False, help_text='State chcange manualy. ', verbose_name='Manual set'),
        ),
    ]
