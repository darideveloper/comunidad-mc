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
