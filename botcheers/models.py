from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User as UserAuth
from django.utils import timezone


class User (models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    name = models.CharField(
        max_length=50, 
        verbose_name='Name',
        help_text='Nambre del usuario', 
        unique=True
    )
    cookies = models.JSONField(
        verbose_name='Cookies', 
        help_text='Cookies de sesión del usuario'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Activo', 
        help_text='Indica si el usuario está activo'
    )
    last_update = models.DateTimeField(
        auto_now=True, 
        verbose_name='Última actualización', 
        help_text='Fecha y hora de la última actualización'
    )
    user_auth = models.ForeignKey(
        UserAuth, 
        on_delete=models.CASCADE, 
        verbose_name='Usuario de autenticación',
        help_text='Usuario de autenticación', 
        null=True, 
        blank=True, 
        related_name='user_auth_cheers'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

class Donation(models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        help_text='Usuario que ha realizado la donación',
        null=True,
        blank=True
    )
    stream_chat_link = models.URLField(
        verbose_name='Enlace al chat del stream',
        help_text='Enlace al chat del stream',
        validators=[
            RegexValidator(
                regex=r'https://www.twitch.tv/popout/.*/chat\?popout=',
                message='El enlace debe ser un un chat de twitch. Ejemplo: https://www.twitch.tv/popout/usuario/chat?popout=',
                code='invalid_characters'
            )
        ]
    )
    time = models.TimeField (
        verbose_name='Hora',
        help_text='Hora de la donación',
        default="00:00:00"
    )
    amount = models.IntegerField(
        verbose_name='Cantidad',
        help_text='Cantidad de la donación'
    )
    message = models.CharField(
        max_length=100,
        verbose_name='Mensaje',
        help_text='Mensaje de la donación'
    )
    done = models.BooleanField(
        default=False,
        verbose_name='Donación realizada',
        help_text='Indica si la donación ha sido enviada al stream'
    )

    def __str__(self):
        return f"{self.user} - {self.amount} bits ({self.user.user_auth.username})"

    class Meta:
        verbose_name = "Donación"
        verbose_name_plural = "Donaciones"


class Token(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        help_text='Apodo del token',
        unique=True
    )
    value = models.CharField(
        max_length=50,
        verbose_name='Valor',
        help_text='Token de validación',
        unique=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el token está activo'
    )

    def __str__(self):
        return f"{self.value} ({self.is_active})"

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"