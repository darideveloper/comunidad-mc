# Generated by Django 4.0.4 on 2023-05-15 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            name='Bot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nambre del usuario', max_length=50, unique=True, verbose_name='Name')),
                ('cookies', models.JSONField(help_text='Cookies de sesión del usuario', verbose_name='Cookies')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el usuario está activo', verbose_name='Activo')),
                ('last_update', models.DateTimeField(auto_now=True, help_text='Fecha y hora de la última actualización', verbose_name='Última actualización')),
                ('user_auth', models.ForeignKey(blank=True, help_text='Usuario de autenticación', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_auth_cheers', to=settings.AUTH_USER_MODEL, verbose_name='Usuario de autenticación')),
            ],
            options={
                'verbose_name': 'Bot',
                'verbose_name_plural': 'Bots',
            },
        ),
    ]
