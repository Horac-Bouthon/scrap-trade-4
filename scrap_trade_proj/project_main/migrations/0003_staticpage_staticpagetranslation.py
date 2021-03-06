# Generated by Django 2.2.6 on 2019-11-21 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_main', '0002_auto_20191120_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idetity', models.CharField(help_text='Identifikation of page', max_length=50, verbose_name='Page identity')),
                ('project', models.ForeignKey(blank=True, help_text='Link to Project', null=True, on_delete=django.db.models.deletion.CASCADE, to='project_main.Project', verbose_name='Project')),
            ],
            options={
                'verbose_name_plural': 'Static pages',
                'verbose_name': 'Static page',
            },
        ),
        migrations.CreateModel(
            name='StaticPageTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German'), ('cs', 'Czech')], max_length=15, verbose_name='language')),
                ('page_name', models.CharField(help_text='Static page name', max_length=50, verbose_name='Page name')),
                ('page_title', models.TextField(blank=True, help_text='Static page title.', null=True, verbose_name='Page title')),
                ('page_body', models.TextField(blank=True, help_text='Static page text.', null=True, verbose_name='Page body')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='project_main.StaticPage', verbose_name='staticpage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
