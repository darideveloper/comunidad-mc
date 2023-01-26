# Add parent folder to path
import os
import sys
import pytz
import random
from django.utils import timezone
from datetime import datetime
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from app.twitch import TwitchApi

# Users to add points
users = [
    "darideveloper", 
    "Maxiast23", 
    "minecuak", 
    "danigempleis", 
    "Lucifer__TV__", 
    "yarawtm", 
    "sauromplays", 
    "el_lenniin", 
    "Raven__gg", 
    "varkcum"
]

# get last stream 
stream = models.Stream.objects.all().order_by('datetime').last()

# Connect to twitch class
twitch_api = TwitchApi ()

# Loop users for add points
for user_name in users: 
    
    # Get user
    user = models.User.objects.filter(user_name=user_name).first()
    
    # Loop for the last 6 days of the week
    for back_days in range (1, 7):
        
        # Randsom number of points in each day
        points_day = random.randrange(1, 11)
        
        # Loop for save each user point
        for _ in range (points_day):
        
            # Calculate back date
            back_date = timezone.now() - timezone.timedelta(days=back_days)
            
            # Save general point
            new_general_point = models.GeneralPoint(datetime=back_date, user=user, stream=stream)
            new_general_point.save()
        
            # save weekly points
            current_weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user).count()
            if current_weekly_points < 60:       
                new_weekly_point = models.WeeklyPoint (general_point=new_general_point)
                new_weekly_point.save()
                
            print (f"Point {user} - {stream} - {back_date}")
    
    # add 10 points today
    for _ in range (10):
        twitch_api.add_point_bg(user, stream, 2)
        print ()


    