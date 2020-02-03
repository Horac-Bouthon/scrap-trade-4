# Generated by Django 2.2.6 on 2020-01-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state_wf', '0016_auto_20200121_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepstate',
            name='ntf_group',
            field=models.CharField(blank=True, choices=[('offer_owners', 'Offer Owners'), ('offer_connect', 'Connected on offer'), ('offer_bound', 'Bount to offer'), ('answer_owners', 'Answer Owners'), ('answer_origin', 'Original offer to answer')], default='offer_owners', help_text='Group for notification sending', max_length=20, null=True, verbose_name='NTF group'),
        ),
        migrations.AddField(
            model_name='stepstate',
            name='send_htf',
            field=models.BooleanField(default=False, help_text='Send notification if this state is activated. ', verbose_name='Send notification'),
        ),
    ]