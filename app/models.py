from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User as UserAuth
from django.core.mail import send_mail
from comunidad_mc.settings import EMAIL_HOST_USER, DEBUG_EMAIL_TO

class Ranking (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del ranking", null=False, blank=False, editable=False)
    name = models.CharField(name='name', verbose_name="nombre", help_text="nombre del ranking", null=False, blank=False, max_length=100)
    points = models.IntegerField(name='points', verbose_name="puntos", help_text="puntos requeridos para el ranking", null=False, blank=False)
    max_streams = models.IntegerField(name='max_streams', verbose_name="máximo de streams", help_text="máximo de streams que puede tener el usuario para el ranking", null=False, blank=False, default=0)
    open_hour = models.TimeField(name='open_hour', verbose_name="hora de schedule", help_text="hora de apertura de agendar stream", null=False, blank=False, default=timezone.now)
     
    @classmethod
    def get_lower(cls):
        return cls.objects.all().order_by('points').first()
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Ranking"
        verbose_name_plural = "Rankings"

class User (models.Model):
    id = models.IntegerField(primary_key=True, name='id', verbose_name="id", help_text="id de twitch", null=False, blank=False, editable=False)
    email = models.EmailField(name='email', verbose_name="email", help_text="email de twitch", null=True, blank=True)
    picture = models.CharField(name='picture', verbose_name="foto", help_text="foto de perfil de twitch", null=False, blank=True, max_length=200)
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
    ranking = models.ForeignKey('Ranking', on_delete=models.SET_NULL, name='ranking', verbose_name="ranking", help_text="ranking del usuario", null=True, blank=True)
    user_auth = models.ForeignKey(UserAuth, on_delete=models.CASCADE, name='user_auth', verbose_name="usuario de autenticación", help_text="usuario del dashboard", null=True, blank=True, default="")
    is_donnor = models.BooleanField(name='is_donnor', verbose_name="donador", help_text="indica si el usuario es donador de bits", default=False)
    first_stream_done = models.BooleanField(name='first_stream_done', verbose_name="primer stream", help_text="indica si el usuario ha realizado su primer stream", default=False)
    referred_user_from = models.ForeignKey('User', on_delete=models.SET_NULL, name='referred_user_from', verbose_name="usuario referido de", help_text="usuario que lo referido", null=True, blank=True)
    send_mail = models.BooleanField(name='send_mail', verbose_name="enviar email", help_text="indica si el usuario quiere recibir emails", default=True)
    last_update_token = models.DateTimeField(name='last_update_token', verbose_name="última actualización de token", help_text="fecha de última actualización de token", default=timezone.now)
    update_tries = models.IntegerField(name='update_tries', verbose_name="intentos de actualización", help_text="cantidad de intentos de actualización de token", null=False, blank=False, default=0)
    
    def __str__(self):
        return f"{self.user_name}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['user_name']
    
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
    is_free = models.BooleanField(name='is_free', verbose_name="free", help_text="indica si el stream es free (no restará puntos)", default=False)
    is_vip = models.BooleanField(name='is_vip', verbose_name="vip", help_text="indica si el stream es vip (único en su hora)", default=False)

    def __str__(self):
        return f"{self.id} - {self.user}"
    
    class Meta:
        verbose_name = "Stream"
        verbose_name_plural = "Streams"
        
class Comment (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del comentario", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho el comentario", null=False, blank=False)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, name='stream', verbose_name="stream", help_text="stream al que pertenece el comentario", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del comentario", default=timezone.now)
    comment = models.TextField(name='comment', verbose_name="comentario", help_text="comentario", null=False, blank=False)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, name='status', verbose_name="estado", help_text="estado del check", null=False, blank=False, default=1)
        
    def __str__(self):
        return f"{self.user}: {self.comment} - stream: {self.stream}"
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        
class Status (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del estado", null=False, blank=False, editable=False)
    name = models.CharField(name='name', verbose_name="nombre", help_text="nombre del estado", null=False, blank=False, max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Estatus"
        verbose_name_plural = "Estatus"
        
class InfoPoint (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id de la información de punto", null=False, blank=False, editable=False)
    info = models.CharField(name='info', verbose_name="información", help_text="información del punto", null=False, blank=False, max_length=100)
    
    def __str__(self):
        return self.info
    
    class Meta:
        verbose_name = "Información de punto"
        verbose_name_plural = "Puntos información"

class GeneralPoint (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del punto", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho el punto", null=False, blank=False)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, name='stream', verbose_name="stream", help_text="stream al que pertenece el punto", null=True, blank=True)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del punto", null=False, blank=False, default=timezone.now)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de puntos", null=False, blank=False, default=1)
    info = models.ForeignKey('InfoPoint', on_delete=models.CASCADE, name='info', verbose_name="información", help_text="información del punto", null=False, blank=False, default=1)
    details = models.TextField (name='details', verbose_name="detalles", help_text="detalles del punto", null=False, blank=True)
    
    def __str__(self):
        return f"{self.user} ({self.amount}): {self.datetime} - stream: {self.stream}"
    
    class Meta:
        verbose_name = "Punto general"
        verbose_name_plural = "Puntos generales"

class WeeklyPoint (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del punto", null=False, blank=False, editable=False)
    general_point = models.ForeignKey('GeneralPoint', on_delete=models.CASCADE, name='general_point', verbose_name="punto general", help_text="punto general al que pertenece el punto", null=False, blank=False)

    def __str__(self):
        return str(self.general_point)
    
    class Meta:
        verbose_name = "Punto semanal"
        verbose_name_plural = "Puntos semanales"
        
class WeeklyPointBackup (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del punto", null=False, blank=False, editable=False)
    general_point = models.ForeignKey('GeneralPoint', on_delete=models.CASCADE, name='general_point', verbose_name="punto general", help_text="punto general al que pertenece el punto", null=False, blank=False)

    def __str__(self):
        return "(copy) "+ str(self.general_point)
    
    class Meta:
        verbose_name = "Punto semanal respaldo"
        verbose_name_plural = "Puntos semanales respaldo"
        
class DailyPoint (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del punto", null=False, blank=False, editable=False)
    general_point = models.ForeignKey('GeneralPoint', on_delete=models.CASCADE, name='general_point', verbose_name="punto general", help_text="punto general al que pertenece el punto", null=False, blank=False)

    def __str__(self):
        return str(self.general_point)
    
    class Meta:
        verbose_name = "Punto diarios"
        verbose_name_plural = "Puntos diarios"
        
class Bit (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id de los bits", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho el punto", null=False, blank=False)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, name='stream', verbose_name="stream", help_text="stream al que pertenece el punto", null=True, blank=True)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de bits", null=False, blank=False)
    details = models.CharField(name='details', verbose_name="detalles", help_text="detalles de los bits", null=False, blank=True, max_length=100)
    timestamp = models.DateTimeField(name='timestamp', verbose_name="fecha y hora", help_text="fecha y hora del punto", null=False, blank=False, default=timezone.now)
    is_bits_done = models.BooleanField(name='is_bits_done', verbose_name="bits donados", help_text="indica si los bits han sido donados", default=False)
    
    def __str__(self):
        return f"{self.amount} bits ({self.user})"
    
    class Meta:
        verbose_name = "Bit"
        verbose_name_plural = "Bits"

class PointsHistory (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del historial", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho el punto", null=False, blank=False)
    general_points_num = models.IntegerField(name='general_points_num', verbose_name="puntos generales totales", help_text="puntos generales hasta el día de hoy", null=False, blank=False)
    general_points_week_num = models.IntegerField(name='general_points_week_num', verbose_name="puntos generales semana", help_text="puntos generales obtenidos a lo largo de la semana", null=False, blank=False)
    week_points_num = models.IntegerField(name='week_points_num', verbose_name="puntos semana", help_text="puntos semanales obtenidos a lo largo de la semana", null=False, blank=False, default=0)
    
    def __str__(self):
        return f"{self.user}"
    
    class Meta:
        verbose_name = "Historial de puntos generales y semanales"
        verbose_name_plural = "Puntos historial"
        
class TopDailyPoint (models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario que ha hecho conseguido 10 puntos diarios", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora en que el usuario consiguió los 10 puntos diarios", auto_now=True)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de puntos diarios", null=False, blank=False, default=10)
    
    def __str__(self):
        return f"{self.user} ({self.amount})"
    
    class Meta:
        verbose_name = "Top"
        verbose_name_plural = "Puntos diarios top"
        
class StreamExtra (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del stream extra", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario al que se le ha asignado el stream extra", null=False, blank=False)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de estreams extra", null=False, blank=False, default=1)
    
    def __str__(self):
        return f"({self.amount}) {self.user}"
    
    class Meta:
        verbose_name = "Stream extra"
        verbose_name_plural = "Streams extra"
        
class StreamVip (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del vip extra", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario  al que se le ha asignado el vip", null=False, blank=False)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de vips", null=False, blank=False, default=1)
    
    def __str__(self):
        return f"({self.amount}) {self.user}"
    
    class Meta:
        verbose_name = "Stream Vip"
        verbose_name_plural = "Streams Vip"
        
class StreamFree (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id del free extra", null=False, blank=False, editable=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, name='user', verbose_name="usuario", help_text="usuario  al que se le ha asignado el free", null=False, blank=False)
    amount = models.IntegerField(name='amount', verbose_name="cantidad", help_text="cantidad de frees", null=False, blank=False, default=1)
    
    def __str__(self):
        return f"({self.amount}) {self.user}"
    
    class Meta:
        verbose_name = "Stream Free"
        verbose_name_plural = "Streams Free"
        
class Settings (models.Model):
    id = models.AutoField(primary_key=True, name='id', verbose_name="id", help_text="id de la configuración", null=False, blank=False, editable=False)
    name = models.CharField(name='name', verbose_name="nombre", help_text="nombre de la configuración", null=False, blank=False, max_length=100, unique=True)
    value = models.CharField(name='value', verbose_name="valor", help_text="valor de la configuración", null=False, blank=False, max_length=100)
    
    def __str__ (self):
        return f"{self.name} ({self.value})"
    
    class Meta:
        verbose_name = "Ajuste"
        verbose_name_plural = "Ajustes"
        
class Log (models.Model):
    origin = models.ForeignKey('LogOrigin', on_delete=models.CASCADE, name='origin', verbose_name="origen", help_text="origen del log", null=False, blank=False)
    datetime = models.DateTimeField(name='datetime', verbose_name="fecha y hora", help_text="fecha y hora del log", null=False, blank=False, default=timezone.now)
    details = models.TextField(name='details', verbose_name="detalles", help_text="detalles del log", null=False, blank=False)
    log_type = models.ForeignKey('LogType', on_delete=models.CASCADE, name='log_type', verbose_name="tipo de log", help_text="tipo de log", null=False, blank=False, default=1)
    
    def save(self, *args, **kwargs):
        
        # Show log in console
        print (f"Log {self.log_type}: {self.origin} ({self.datetime}): {self.details}")
        
        exclude_details = ["Invalid OAuth token"]
        
        # Submit error emails
        if self.log_type.id == 2 and self.details not in exclude_details:
            
            send_mail(
                f"Error Comunidad MC ({self.origin})",
                f"origin: {self.origin}\ndatetime: {self.datetime}\ndetails: {self.details}\nlog_type: {self.log_type}",
                EMAIL_HOST_USER,
                [DEBUG_EMAIL_TO],
                fail_silently=False,
            )

        super(Log, self).save(*args, **kwargs)
    
    def __str__ (self):
        return f"{self.origin} ({self.datetime})"

class LogType (models.Model):
    name = models.CharField(name='name', verbose_name="nombre", help_text="nombre del tipo de log", null=False, blank=False, max_length=100)

    def __str__ (self):
        return f"{self.name}"

class LogOrigin (models.Model):
    name = models.CharField(name='name', verbose_name="nombre", help_text="nombre del origen del log", null=False, blank=False, max_length=100)

    def __str__ (self):
        return f"{self.name}"

class ScheduleStreams(models.Model):
    id = models.AutoField(
        primary_key=True, 
        name='id', 
        verbose_name="id", 
        help_text="id del stream programado", 
        null=False, 
        blank=False, 
        editable=False
    )
    user = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        name='user', 
        verbose_name="usuario", 
        help_text="usuario que ha agendado el stream", 
        null=False, 
        blank=False
    )
    start_date = models.DateField(
        name='start_date', 
        verbose_name="fecha y hora de inicio", 
        help_text="fecha y hora de inicio de stream agendados", 
        null=False, 
        blank=False 
    )
    end_date = models.DateField(
        name='end_date', 
        verbose_name="fecha y hora de fin", 
        help_text="fecha y hora de fin de streams agendados", 
        null=False, 
        blank=False
    )
    monday = models.BooleanField(
        name='monday', 
        verbose_name="lunes", 
        help_text="indica si el stream está agendado para los lunes", 
        default=True
    )
    tuesday = models.BooleanField(
        name='tuesday', 
        verbose_name="martes", 
        help_text="indica si el stream está agendado para los martes", 
        default=True
    )
    wednesday = models.BooleanField(
        name='wednesday', 
        verbose_name="miércoles", 
        help_text="indica si el stream está agendado para los miércoles", 
        default=True
    )
    thursday = models.BooleanField(
        name='thursday', 
        verbose_name="jueves", 
        help_text="indica si el stream está agendado para los jueves", 
        default=True
    )
    friday = models.BooleanField(
        name='friday', 
        verbose_name="viernes", 
        help_text="indica si el stream está agendado para los viernes", 
        default=True 
    )
    saturday = models.BooleanField(
        name='saturday', 
        verbose_name="sábado", 
        help_text="indica si el stream está agendado para los sábados", 
        default=True
    )
    time = models.TimeField(
        name='time', 
        verbose_name="hora", 
        help_text="hora de inicio de stream agendados", 
        null=False, 
        blank=False
    )
    
    def save(self, *args, **kwargs):
        # Remove minutes and seconds from time
        self.time = self.time.replace(minute=0, second=0)
        
        # Save schedule streams
        available_weekdays = []
        if self.monday:
            available_weekdays.append(0)
        if self.tuesday:
            available_weekdays.append(1)
        if self.wednesday:
            available_weekdays.append(2)
        if self.thursday:
            available_weekdays.append(3)
        if self.friday:
            available_weekdays.append(4)
        if self.saturday:
            available_weekdays.append(5)
        
        for days in range((self.end_date - self.start_date).days + 1):
            date = self.start_date + timedelta(days=days)
            if date.weekday() in available_weekdays:
                Stream.objects.create(
                    user=self.user,
                    datetime=timezone.make_aware(datetime.combine(date, self.time), timezone.get_current_timezone()),
                )
        
        # Default save
        super(ScheduleStreams, self).save(*args, **kwargs)
    
    def __str__ (self):
        return f"{self.start_date} - {self.end_date}"
    
    class Meta:
        verbose_name = "Stream programado"
        verbose_name_plural = "Streams programados"
