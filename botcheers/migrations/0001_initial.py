# Generated by Django 4.0.4 on 2023-05-14 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_chat_link', models.URLField(help_text='Enlace al chat del stream', verbose_name='Enlace al chat del stream')),
                ('hour', models.IntegerField(help_text='Hora de la donación', verbose_name='Hora')),
                ('minute', models.IntegerField(help_text='Minuto de la donación', verbose_name='Minuto')),
                ('amount', models.IntegerField(help_text='Cantidad de la donación', verbose_name='Cantidad')),
                ('message', models.CharField(help_text='Mensaje de la donación', max_length=100, verbose_name='Mensaje')),
                ('status', models.BooleanField(default=False, help_text='Indica si la donación ha sido procesada', verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Donación',
                'verbose_name_plural': 'Donaciones',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Apodo del token', max_length=50, unique=True, verbose_name='Nombre')),
                ('value', models.CharField(help_text='Token de validación', max_length=50, unique=True, verbose_name='Valor')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el token está activo', verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nambre del usuario', max_length=50, unique=True, verbose_name='Name')),
                ('cookies', models.JSONField(help_text='Cookies de sesión del usuario', verbose_name='Cookies')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el usuario está activo', verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, help_text='Fecha y hora de la última actualización', verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
    ]