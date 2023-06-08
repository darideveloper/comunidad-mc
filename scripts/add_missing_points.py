# Conver today general points with amount in 0, to weekly points with amount in 1, and save them as week points

# Add parent folder to path
import os
import sys
import random
from datetime import timedelta
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from django.utils import timezone
from app import models

# UPDATE THIS
streamers = [
    "Soy_Jorge_8a",
    "timbomx",
]

users = models.User.objects.all ()

for streamer in streamers:
    
    # Get last stream of today
    today = timezone.now ().replace (hour=0, minute=0, second=0, microsecond=0)
    stream = models.Stream.objects.filter (user__user_name=streamer, datetime__gte=today).order_by ('datetime').first ()

    for user in users:
        
        print (f"Adding points to {user.user_name} in {stream}")
        
        # Add general to each user
        general_point = models.GeneralPoint (
            user=user, 
            stream=stream, 
            datetime=stream.datetime, 
            info=models.InfoPoint.objects.get (info="ver stream"), 
            amount=1
        )
        general_point.save ()
        
        # Add daily to each user
        models.DailyPoint (general_point=general_point).save ()
    