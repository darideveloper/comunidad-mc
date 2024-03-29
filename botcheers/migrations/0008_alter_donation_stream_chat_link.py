# Generated by Django 4.0.4 on 2023-05-22 07:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botcheers', '0007_alter_donation_stream_chat_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='stream_chat_link',
            field=models.URLField(help_text='Enlace al chat del stream', validators=[django.core.validators.RegexValidator(code='invalid_characters', message='El enlace debe ser un un chat de twitch. Ejemplo: https://www.twitch.tv/popout/usuario/chat?popout=', regex='https://www.twitch.tv/popout/.*/chat\\?popout=')], verbose_name='Enlace al chat del stream'),
        ),
    ]
