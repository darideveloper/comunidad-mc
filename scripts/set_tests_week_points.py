# Add parent folder to path
import os
import sys
import pytz
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

# Load environment variables
load_dotenv ()
WEEK_POINTS = int(os.getenv('SCRIPTS_WEEK_POINTS'))
USER_NAME = os.getenv('SCRIPTS_USER_NAME')

# Get user instance and last stream
user = models.User.objects.filter(user_name=USER_NAME).first()
stream = models.Stream.objects.all().order_by('datetime').last()

# Delete old points
print ("Deleting old points...")
models.GeneralPoint.objects.filter (user=user).delete()

# Loop for each day of the week
for back_days in range (7):
    
    # Loop for save each user point
    for _ in range (WEEK_POINTS):
    
        # Calculate back date
        back_date = timezone.now() - timezone.timedelta(days=back_days)
        
        # Save general point
        new_general_point = models.GeneralPoint(datetime=back_date, user=user, stream=stream)
        new_general_point.save()
        
        # Save daily points
        current_daily_points = models.DailyPoint.objects.filter(general_point__user=user).count()
        if current_daily_points < 10 and back_days == 6:            
            new_daily_point = models.DailyPoint (general_point=new_general_point)
            new_daily_point.save()
    
        # save weekly points
        current_weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user).count()
        if current_weekly_points < 60:       
            new_weekly_point = models.WeeklyPoint (general_point=new_general_point)
            new_weekly_point.save()
            
        print (f"Point {user} - {stream} - {back_date}")

    