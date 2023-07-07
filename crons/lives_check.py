""" Check if streamr has open streams in time and add negative points """

# Add parent folder to path
import os
import sys
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.twitch import TwitchApi
from app import tools
from app import models


log_origin_name = "Lives Check"
try:
    # Get live streams
    twitch = TwitchApi (log_origin_name)
    streams = twitch.get_current_streams ()

    # Validate if each stream is live
    for stream in streams:
        
        # Get user and live status
        user = stream.user
        is_live = twitch.is_user_live (user)
            
        if not is_live:        
            # Add negative points
            tools.set_negative_point (user, 50, "penalización por no abrir stream a tiempo", stream)
                    
            # Delete stream
            stream.delete()
            
except Exception as e:
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )
    