# Generated by Django 4.0.4 on 2022-12-19 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_last login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last login',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='user last login', verbose_name='last login'),
        ),
    ]
