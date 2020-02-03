# Generated by Django 2.2.6 on 2020-01-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_messtemp_messtemptranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='messtemp',
            name='temp_type',
            field=models.CharField(blank=True, choices=[('text', 'Text'), ('html', 'Html')], default='text', help_text='Template type (text/html)', max_length=20, null=True, verbose_name='Template type'),
        ),
    ]