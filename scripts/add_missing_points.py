# Add or update a general and daily pont to all users, in speciic streams

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
    "gamora_0292",
]

users = models.User.objects.all ()

for streamer in streamers:
    
    # Get last stream of today
    today = timezone.now ().replace (hour=0, minute=0, second=0, microsecond=0)
    stream = models.Stream.objects.filter (user__user_name=streamer, datetime__gte=today).order_by ('datetime').first ()

    for user in users:
        
        # Validate if already have points
        point = models.GeneralPoint.objects.filter (user=user, stream=stream)
        if point:
            
            print (f"Updating points to {user.user_name} in {stream}")
            
            # Update point data
            general_point = point.first ()
            if general_point.amount == 0:
                general_point.amount = 1
            general_point.info = models.InfoPoint.objects.get (info="ver stream")
            general_point.save ()
        else:
        
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
            
        # Validate if already have daily points
        daily_point = models.DailyPoint.objects.filter (general_point=general_point)
        if not daily_point:
            
            print (f"Adding daily points to {user.user_name} in {stream}")            
            
            # Add daily to each user
            models.DailyPoint (general_point=general_point).save ()
    