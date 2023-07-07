# Set specific general and today points to all users, in specific stream

# UPDATE THIS:
STREAMS_IDS = [2919, 2916]
POINTS = 1

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
from app import models
from app.twitch import TwitchApi

users = models.User.objects.all()

# Connect to twitch class
twitch_api = TwitchApi ("Script")

# Get streamers
streams = models.Stream.objects.filter(id__in=STREAMS_IDS)

for stream in streams:

    print (f"\nStream: {stream}\n")

    # Loop users for add points
    for user_name in users: 
        
        # Get user
        user = models.User.objects.filter(user_name=user_name).first()
        
        # Skip if user not found
        if not user:
            continue
        
        # Delete if user already have a point in the stream
        models.GeneralPoint.objects.filter(user=user, stream=stream).delete ()
        
        # add 10 points today
        for _ in range (POINTS):
            twitch_api.add_point(user, stream, force=True)
    