# Add parent folder to path
import os
import sys
import pytz
from django.utils import timezone
from datetime import datetime
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models

# Options
week_points = 12
user_name = 'darideveloper3'

# Get user instance and last stream
user = models.User.objects.filter(user_name=user_name).first()
stream = models.Stream.objects.all().order_by('datetime').last()

# Delete old points
print ("Deleting old points...")
models.GeneralPoint.objects.filter (user=user).delete()

# Loop for each day of the week
for back_days in range (7):
    
    # Loop for save each user point
    for _ in range (week_points):
    
        # Calculate back date
        back_date = timezone.now() - timezone.timedelta(days=back_days)
        
        # Save general point
        new_general_point = models.GeneralPoint(datetime=back_date, user=user, stream=stream)
        new_general_point.save()
        
        # Save daily points
        current_daily_points = models.DailyPoint.objects.filter(general_point__user=user).count()
        if current_daily_points < 10:            
            new_daily_point = models.DailyPoint (general_point=new_general_point)
            new_daily_point.save()
    
        # save weekly points
        current_weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user).count()
        if current_weekly_points < 60:       
            new_weekly_point = models.WeeklyPoint (general_point=new_general_point)
            new_weekly_point.save()
            
        print (f"Point {user} - {stream} - {back_date}")

    