# Generated by Django 4.0.4 on 2023-03-09 22:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_rename_bits_bit'),
    ]

    operations = [
        migrations.AddField(
            model_name='bit',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='fecha de los bits', verbose_name='fecha'),
        ),
    ]
