""" Read chat from twitch streams who are live (in system) """

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

from app.twitch import TwitchApi

log_origin_name = "Read Chat"
try:
    # Submit data to nodejs api, for start reading chat
    twitch = TwitchApi (log_origin_name)
    twitch.submit_streams_node()
except Exception as e:
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )