from django.db import models
from django.utils import timezone

class User (models.Model):
    id = models.IntegerField(primary_key=True, name='id', verbose_name="id", help_text="id de twitch", null=False, blank=False, editable=False)
    email = models.EmailField(name='email', verbose_name="email", help_text="email de twitch", null=False, blank=True)
    picture = models.URLField(name='picture', verbose_name="foto", help_text="foto de perfil de twitch", null=False, blank=True)
    user_name = models.CharField(name='user_name', verbose_name="usuario", help_text="nombre de usuario de twitch", null=False, blank=True, max_length=100)
    access_token = models.CharField(name='access_token', verbose_name="access token", help_text="access token generado por twitch", null=False, blank=False, max_length=50)
    refresh_token = models.CharField(name='refresh_token', verbose_name="refresh token", help_text="refresh token generado por twitch", null=False, blank=False, max_length=50)
    last_login = models.DateTimeField(name='last_login', verbose_name="últimos login", help_text="fecha de último inicio de sesión", default=timezone.now)
    first_name = models.CharField(name='first_name', verbose_name="nombre", help_text="nombre real del usuario", null=True, blank=True, max_length=100)
    last_name = models.CharField(name='last_name', verbose_name="apellido", help_text="apellido real del usuario", null=True, blank=True, max_length=100)
    country = models.CharField(name='country', verbose_name="país", help_text="país de residencia", null=True, blank=True, max_length=100)
    phone = models.CharField(name='phone', verbose_name="teléfono", help_text="teléfono con código de país", null=True, blank=True, max_length=20)
    time_zone = models.CharField(name='time_zone', verbose_name="zona horaria", help_text="zona horaria de residencia", null=True, blank=True, max_length=100)
    is_active = models.BooleanField(name='is_active', verbose_name="activo", help_text="indica si el usuario está activo", default=False)
    
    def __str__(self):
        email = self.email if self.email else "no email"
        return f"{self.id} - {self.user_name} - {email}"