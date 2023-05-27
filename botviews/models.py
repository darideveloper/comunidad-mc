from django.db import models
from app import models as app_models

class User (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Name', help_text='Nambre del usuario', unique=True)
    cookies = models.JSONField(verbose_name='Cookies', help_text='Cookies de sesión del usuario')
    is_active = models.BooleanField(default=True, verbose_name='Activo', help_text='Indica si el usuario está activo')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización', help_text='Fecha y hora de la última actualización')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

class Proxy (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    host = models.CharField(max_length=50, verbose_name='Host', help_text='Host del proxy')
    port = models.IntegerField(verbose_name='Puerto', help_text='Puerto del proxy')
    user = models.CharField(max_length=50, verbose_name='Usuario', help_text='Usuario del proxy', default='')
    password = models.CharField(max_length=50, verbose_name='Contraseña', help_text='Contraseña del proxy', default='')
    
    def __str__(self):
        return f"{self.host}:{self.port}"
    
    class Meta:
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"
        
class Setting (models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', help_text='Nombre de la configuración', unique=True)
    value = models.CharField(max_length=50, verbose_name='Valor', help_text='Valor de la configuración')
    
    def __str__ (self):
        return f"{self.name} ({self.value})"
    
    class Meta:
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"
        
class Token (models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', help_text='Apodo del token', unique=True)
    value = models.CharField(max_length=50, verbose_name='Valor', help_text='Token de validación', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Activo', help_text='Indica si el token está activo')
    
    def __str__ (self):
        return f"{self.value} ({self.is_active})"
    
    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
    