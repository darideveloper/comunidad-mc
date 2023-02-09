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
from app import models

# Get live streams
twitch = TwitchApi ()
streams = twitch.get_current_streams ()

# Validate if each stream is live
for stream in streams:
    
    # Get user and live status
    user = stream.user
    is_live = twitch.is_user_live (user)
    
    # Add negative points if stream is not live
    if not is_live:
        
        print (f"Adding negative points to {user} for not opening stream in time, and removing from list")
        
        info_point = models.InfoPoint.objects.get (info="penalización por no abrir stream a tiempo")
        general_point = models.GeneralPoint (
            user=user, datetime=timezone.now(), amount=-50, info=info_point)
        general_point.save ()
        
        # Delete stream
        stream.delete()
    