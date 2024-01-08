""" Set points to the users in the current streams """

# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.twitch import TwitchApi
from app import models

log_origin_name = "Calculate Points"
try:
    # Submit data to nodejs api, for start reading chat
    twitch = TwitchApi (log_origin_name)

    # Get streams
    current_streams = twitch.get_current_streams()

    # Calculate points
    twitch.calculate_points(current_streams)
except Exception as e:
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )