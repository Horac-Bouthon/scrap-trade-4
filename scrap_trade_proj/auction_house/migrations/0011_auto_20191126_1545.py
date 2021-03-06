# Generated by Django 2.2.6 on 2019-11-26 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction_house', '0010_ahmatclasstranslation'),
    ]

    operations = [
        migrations.AddField(
            model_name='ahofferline',
            name='mat_class',
            field=models.ForeignKey(blank=True, help_text='Link to Material class', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_lines', to='auction_house.AhMatClass', verbose_name='Material class'),
        ),
        migrations.AlterField(
            model_name='ahmatclasstranslation',
            name='display_name',
            field=models.CharField(blank=True, help_text='Name of the material class for displaying', max_length=200, null=True, verbose_name='Material class display name'),
        ),
    ]
