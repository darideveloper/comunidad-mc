# Generated by Django 4.0.4 on 2023-08-07 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0096_alter_topdailypoint_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='email de twitch', max_length=254, null=True, verbose_name='email'),
        ),
    ]