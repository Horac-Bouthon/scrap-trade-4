# Generated by Django 2.2.6 on 2020-02-03 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('state_wf', '0019_merge_20200131_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stepstate',
            name='ntf_group',
        ),
    ]