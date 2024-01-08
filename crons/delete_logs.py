# Update all users tokens if is invalid
import requests

# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from django.utils import timezone

try:

    log_origin = models.LogOrigin.objects.get (name="Delete Logs")
    log_type_error = models.LogType.objects.get (name="error")
    log_type_info = models.LogType.objects.get (name="info")

    # Detect old logs
    now = timezone.now()
    last_monday = now - timezone.timedelta(days=now.weekday())
    last_monday = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    logs_old = models.Log.objects.all ().filter(datetime__lt=last_monday)
    logs_num = logs_old.count ()
    logs_old.delete ()

    models.Log.objects.create (
        origin = log_origin,
        details = f"Deleted {logs_num} logs",
        log_type = log_type_info
    )
    
except Exception as err:

    models.Log.objects.create (
        origin = log_origin,
        details = f"Error: {err}",
        log_type = log_type_error
    )