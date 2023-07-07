# Set specific general and today points to all users, in specific stream

# UPDATE THIS:
STREAMER_NAME = "darideveloper2"
POINTS = 5

# Add parent folder to path
import os
import sys
import random
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
streamer = models.User.objects.filter(user_name=STREAMER_NAME).first ()

# Get last streams of streamer
stream = models.Stream.objects.filter(user=streamer).order_by('-id').first()
print (f"\nStream: {stream}\n")

# Loop users for add points
for user in users: 
    
    print (f"Adding points to {user.user_name} in {stream}")

    general_point = models.GeneralPoint (
        user=user,
        stream=stream,
        amount=POINTS,
        info=models.InfoPoint.objects.get (info="ver stream"),
    )
    general_point.save ()
    
    models.DailyPoint.objects.create (
        general_point=general_point
    )
