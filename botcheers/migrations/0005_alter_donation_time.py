# Generated by Django 4.0.4 on 2023-05-22 06:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('botcheers', '0004_remove_donation_hour_remove_donation_minute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, help_text='Hora de la donación', verbose_name='Hora'),
        ),
    ]
