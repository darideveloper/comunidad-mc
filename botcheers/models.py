from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User as UserAuth
from django.utils import timezone


class User (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(
        max_length=50, 
        verbose_name='Name',
        help_text='Nambre del usuario', 
        unique=True
    )
    password = models.CharField(
        max_length=50,
        verbose_name='Contraseña',
        help_text='Contraseña del usuario',
        default='ComunidadMC'
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
    datetime = models.DateTimeField(
        verbose_name='Fecha y hora',
        help_text='Fecha y hora de la donación',
        default=timezone.now
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
        
class Proxy(models.Model):
    id = models.AutoField(
        primary_key=True, 
        verbose_name='ID'
    )
    host = models.CharField(
        max_length=50, 
        verbose_name='Host', 
        help_text='Host del proxy'
    )
    port = models.IntegerField(
        verbose_name='Puerto', 
        help_text='Puerto del proxy'
    )
    
    def __str__(self):
        return f"{self.host}:{self.port}"
    
    class Meta:
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"
        
class BitsHistory (models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    ),
    datetime = models.DateTimeField(
        verbose_name='Fecha y hora',
        default=timezone.now
    ),
    donation = models.ForeignKey(
        'Donation',
        on_delete=models.CASCADE,
        name='Donación',
        help_text='Donación asociada al historial',
        null=True,
        blank=True,
    ),
    amount = models.IntegerField(
        verbose_name='Cantidad',
        null=True,
        blank=True,
        default=0
    )
    
    def save(self, *args, **kwargs):
        
        # Get or create bit summary
        bit_summary = BitsSummary.objects.get_or_create(
            bot=self.donation.user
        )        
        # Get bot and amounts
        bot = self.donation.user
        amount_donation = self.donation.amount
        amount_history = self.amount
        
        # Save negative amount if donation is done
        donation_done = self.donation.done
        if donation_done:
            bit_summary.balance -= amount_donation
        
        # Save amount from history
        if amount_history:
            bit_summary.balance += amount_history
            
        # Save summary
        bit_summary.last_update = self.datetime
        bit_summary.save()
        
        super(BitsHistory, self).save(*args, **kwargs)
        
    def __str__ (self):
        return self.id
    
    class Meta:
        verbose_name = "Historial de bits"
        verbose_name_plural = "Historiales de bits"

class BitsSummary (models.Model):
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    ),
    bot = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        help_text='Bot de bits',
    ),
    last_update = models.DateTimeField(
        verbose_name='Fecha y hora',
        default=timezone.now
    ),
    balance = models.IntegerField(
        verbose_name='Balance',
        default=0
    )
    
    def __str__ (self):
        return self.id
    
    class Meta:
        verbose_name = "Resumen de bits"
        verbose_name_plural = "Resúmenes de bits"