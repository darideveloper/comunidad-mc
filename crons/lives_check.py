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
from app.logs import logger
from app import tools

logs_prefix = "lives check -"

# Get live streams
twitch = TwitchApi (logs_prefix=logs_prefix)
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
        logger.info (f"{logs_prefix} delete stream {stream}")
        stream.delete()
    