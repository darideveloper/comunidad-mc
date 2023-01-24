# Add parent folder to path
import os
import sys
import datetime
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

# Dejango imports
from app.models import WeeklyPoint, DailyPoint
from django.utils import timezone

# Load environment variables
load_dotenv ()
RESTART_POINTS_WEEK_DAY = int(os.getenv('RESTART_POINTS_WEEK_DAY'))

# Get current week day
now = timezone.now()
today = now.weekday()

# delete all weekly points
if today == RESTART_POINTS_WEEK_DAY:    
    WeeklyPoint.objects.all().delete()
    print ("week points deleted")
    
# delete all daily points
DailyPoint.objects.all().delete()
print ("today points deleted")