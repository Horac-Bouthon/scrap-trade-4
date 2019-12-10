# Generated by Django 2.2.6 on 2019-10-09 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_projectcustomuser_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcustomuser',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active user'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='access admin'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='name',
            field=models.CharField(max_length=255, verbose_name='user name'),
        ),
    ]
