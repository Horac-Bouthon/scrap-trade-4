# Generated by Django 2.2.6 on 2019-10-10 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20191009_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcustomuser',
            name='email',
            field=models.EmailField(help_text='Required: 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='User can log in', verbose_name='active user'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='User can access administration tools', verbose_name='access admin tools'),
        ),
        migrations.AlterField(
            model_name='projectcustomuser',
            name='name',
            field=models.CharField(help_text='User identification', max_length=255, verbose_name='user name'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
