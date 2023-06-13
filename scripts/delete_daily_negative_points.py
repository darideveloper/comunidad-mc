# Add or update a general and daily pont to all users, in speciic streams

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
users = models.User.objects.all ()

print ("Deleting negative points...")

for user in users:
    
    daily_points_negative = models.DailyPoint.objects.filter (
        general_point__user=user,
        general_point__amount__lt=0,
    )
    
    for point in daily_points_negative:
    
        point.delete ()        
        print (f"{user.user_name} {point.general_point.amount} negative points deleted")
        