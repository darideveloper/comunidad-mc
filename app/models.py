from django.db import models
from django.utils import timezone

# Create your models here.
class User (models.Model):
    id = models.IntegerField(primary_key=True, name='id', verbose_name="id", help_text="user twitch id", null=False, blank=False)
    email = models.EmailField(name='email', verbose_name="email", help_text="user email", null=False, blank=True)
    picture = models.URLField(name='picture', verbose_name="picture", help_text="user picture", null=False, blank=True)
    name = models.CharField(name='name', verbose_name="name", help_text="user name", null=False, blank=True, max_length=100)
    access_token = models.CharField(name='access token', verbose_name="access token", help_text="user access token", null=False, blank=False, max_length=50)
    refresh_token = models.CharField(name='refresh token', verbose_name="refresh token", help_text="user refresh token", null=False, blank=False, max_length=50)
    last_login = models.DateTimeField(name='last login', verbose_name="last login", help_text="user last login", default=timezone.now)
    
    def __str__(self):
        email = self.email if self.email else "no email"
        return f"{self.id} - {self.name} - {email}"