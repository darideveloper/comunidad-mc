import datetime
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
    country = models.ForeignKey('Country', on_delete=models.CASCADE, name='country', verbose_name="país", help_text="país de residencia", null=True, blank=True)
    phone = models.CharField(name='phone', verbose_name="teléfono", help_text="teléfono con código de país", null=True, blank=True, max_length=20)
    time_zone = models.ForeignKey('TimeZone', on_delete=models.CASCADE, name='time_zone', verbose_name="zona horaria", help_text="zona horaria", null=True, blank=True)
    is_active = models.BooleanField(name='is_active', verbose_name="activo", help_text="indica si el usuario ha validado su cuenta con whatsapp", default=False)

    def __str__(self):
        email = self.email if self.email else "no email"
        return f"({self.id}) {self.user_name}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
class TimeZone (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id de la zona horaria", null=False, blank=False, editable=False)
    time_zone = models.CharField(name='time_zone', verbose_name="zona horaria", help_text="zona horaria", null=False, blank=False, max_length=100)

    def __str__(self):
        return self.time_zone
    
    class Meta:
        verbose_name = "Zona Horaria"
        verbose_name_plural = "Zonas Horarias"

class Country (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del país", null=False, blank=False, editable=False)
    country = models.CharField(name='country', verbose_name="país", help_text="país de residencia", null=False, blank=False, max_length=100)

    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        
class Stream (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del stream", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que está transmitiendo", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del stream", null=False, blank=False, default=timezone.now)
    
    def __str__(self):
        formated_date = str(timezone.localtime(self.datetime))[0:-12] + "h"
        return f"{self.user.user_name} {formated_date}"
    
    class Meta:
        verbose_name = "Stream"
        verbose_name_plural = "Streams"
        
class Comment (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del comentario", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho el comentario", null=False, blank=False)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, name='stream', verbose_name="stream", help_text="stream al que pertenece el comentario", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del comentario", null=False, blank=False, default=timezone.now)
    comment = models.TextField(name='comment', verbose_name="comentario", help_text="comentario", null=False, blank=False)
    
    def __str__(self):
        return f"{self.user}: {self.comment} - {self.stream.user.user_name}"
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        
class WhatchCheck (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del check", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que asistió al stream", null=False, blank=False)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, name='stream', verbose_name="stream", help_text="stream al que pertenece el check", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del check", null=False, blank=False, default=timezone.now)
    
    def __str__(self):
        return f"{self.user}: {self.datetime} - {self.stream.user.user_name}"
    
    class Meta:
        verbose_name = "Check"
        verbose_name_plural = "Checks"