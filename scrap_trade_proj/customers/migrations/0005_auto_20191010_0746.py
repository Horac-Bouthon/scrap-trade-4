# Generated by Django 2.2.6 on 2019-10-10 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20191010_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='static/images/profile_pics'),
        ),
    ]
