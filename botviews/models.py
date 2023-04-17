from django.db import models

class User (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Name', help_text='Nambre del usuario')
    cookies = models.JSONField(verbose_name='Cookies', help_text='Cookies de sesión del usuario')
    is_active = models.BooleanField(default=True, verbose_name='Activo', help_text='Indica si el usuario está activo')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Proxy (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    host = models.CharField(max_length=50, verbose_name='Host', help_text='Host del proxy')
    port = models.IntegerField(verbose_name='Puerto', help_text='Puerto del proxy')
    user = models.CharField(max_length=50, verbose_name='Usuario', help_text='Usuario del proxy')
    password = models.CharField(max_length=50, verbose_name='Contraseña', help_text='Contraseña del proxy')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, verbose_name='Ubicación', help_text='Ubicación del proxy', null=True, blank=True)
    
    def __str__(self):
        return f"{self.host}:{self.port}"
    
    class Meta:
        verbose_name = "Proxy"
        verbose_name_plural = "Proxies"
    
class Location (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Nombre', help_text='Nombre de la ubicación', unique=True)
    
    def __str__ (self):
        return self.name
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        
class Settings (models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', help_text='Nombre de la configuración', unique=True)
    value = models.CharField(max_length=50, verbose_name='Valor', help_text='Valor de la configuración')
    
    def __str__ (self):
        return f"{self.name} ({self.value})"
    
    class Meta:
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"