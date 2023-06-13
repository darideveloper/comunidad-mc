# delete extra daily points in all users

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
    
users = models.User.objects.all ()

for user in users:
            
    # Validate if already have points
    daily_points = models.DailyPoint.objects.filter (general_point__user=user)
    
    # Validate if have more than 10 points
    if daily_points.count () > 10:
        
        # Select the extra points
        extra_points = daily_points[10:]
        
        # Delete extra points
        for point in extra_points:
            point.delete ()
            
        extra_points_num = extra_points.count ()
        current_points_num = daily_points.count ()
        
        print (f"{extra_points_num} extra points deleted from {user.user_name}, now have {current_points_num} points")