# Set specific general and today points to all users, in specific stream

# UPDATE THIS:
SREAMS_IDS = [4918]
POINTS = 1
DAILY_POINT = True
WEEKLY_POINT = False 

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

users = models.User.objects.all()

# Connect to twitch class
twitch_api = TwitchApi ("Script")

# Get streamers
streams = models.Stream.objects.filter (id__in=SREAMS_IDS)

# Get last streams of streamer
for stream in streams:
    print (f"\nStream: {stream}\n")

    # Loop users for add points
    for user in users: 
        
        # Delete old general point
        general_point = models.GeneralPoint.objects.filter (
            stream=stream,
            user=user,
        ).delete ()
        
        message = f"adding {POINTS} general"
        if DAILY_POINT:
            message += " and daiy"
        if WEEKLY_POINT:
            message += " and weekly"
        message += f" points to user {user.user_name} in {stream}"
        models.Log.objects.create (
            origin=models.LogOrigin.objects.get (name="Script"),
            details=message,
        )
        
        general_point = models.GeneralPoint (
            user=user,
            stream=stream,
            amount=POINTS,
            info=models.InfoPoint.objects.get (info="ver stream"),
        )
        general_point.save ()
        
        if DAILY_POINT: 
            models.DailyPoint.objects.create (
                general_point=general_point
            )
            print (f"Added {POINTS} daily points to {user.user_name}")
            
        if WEEKLY_POINT:
            models.WeeklyPoint.objects.create (
                general_point=general_point
            )
            print (f"Added {POINTS} weekly points to {user.user_name}")
