# Add or update a general and daily pont to all users, 
# in speciic streams, with optional adding tripple points,
# or creating points if not exists

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
triple_time = True
streams_ids = [
    "2732"
]
users = models.User.objects.all ()

for stream_id in streams_ids:
    
    # Get last stream with id
    stream = models.Stream.objects.get (id=stream_id)
    
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
            
            # Add triple time points
            if triple_time:
                print (f"Adding triple time points to {user.user_name} in {stream}")
                
                triple_time_point = models.GeneralPoint.objects.create (
                    user=user, 
                    stream=stream, 
                    info= models.InfoPoint.objects.get (info="ver stream (puntos extra)"),
                    amount=2
                )
             
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
