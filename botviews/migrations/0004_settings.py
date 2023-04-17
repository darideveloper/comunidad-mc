# Generated by Django 4.0.4 on 2023-04-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botviews', '0003_rename_locations_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre de la configuración', max_length=50, unique=True, verbose_name='Nombre')),
                ('value', models.CharField(help_text='Valor de la configuración', max_length=50, verbose_name='Valor')),
            ],
        ),
    ]
