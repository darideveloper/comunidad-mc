# Add or update a general and daily pont to all users, in speciic streams

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
from django.utils import timezone
from app import models
from dotenv import load_dotenv

load_dotenv ()
MAX_DAILY_POINTS = int (os.getenv ("MAX_DAILY_POINTS"))

# UPDATE THIS
create_points = False
streamers = [
    "Lucifer__TV__",
    "Jelay28",
    "popetalove",
    "elkin161",
    "kurolaos",
    "jeza1989",
    "goldstk",
    "SrOscuro_",
    "Kerjos_",
    "Danncrimson",
    "PaquilloMad",
]


users = models.User.objects.all ()

for streamer in streamers:
    
    
    # Get last stream of today
    today = timezone.now ().replace (hour=0, minute=0, second=0, microsecond=0)
    start_date = today.replace (hour=0, minute=0, second=0, microsecond=0)
    end_date = today.replace (hour=23, minute=59, second=59, microsecond=999999)
    stream = models.Stream.objects.filter (user__user_name=streamer, datetime__range=(start_date, end_date)).order_by ("-datetime").first ()
    
    if not stream:
        continue

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
            
            point_added = True
            
        else:
            
            if not create_points:
                continue
        
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
            
            point_added = True
        
        # Validate if already have daily points
        daily_point = models.DailyPoint.objects.filter (general_point=general_point)
        if daily_point:
            print (f"Already have daily points to {user.user_name} in {stream}")
            continue
            
        # Validate max daily points 
        daily_points_num = models.DailyPoint.objects.filter (general_point__user=user).count ()
        if daily_points_num >= MAX_DAILY_POINTS:
            print (f"Already have {daily_points_num} daily points")
            continue
            
        # Add daily to user
        print (f"Adding daily points to {user.user_name} in {stream}")            
        models.DailyPoint (general_point=general_point).save ()
