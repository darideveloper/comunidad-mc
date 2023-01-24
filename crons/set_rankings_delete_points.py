# Add parent folder to path
import os
import sys
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

# Django imports
from django.utils import timezone
from app.models import User, Ranking, WeeklyPoint, DailyPoint
from app.logs import logger

# Get ranbkings and required points
rankings = Ranking.objects.all().order_by("points").reverse()

# Load environment variables
load_dotenv ()
RESTART_POINTS_WEEK_DAY = int(os.getenv('RESTART_POINTS_WEEK_DAY'))
DEBUG = os.getenv('DEBUG')

# Overwrite restart date in debug mode
if DEBUG == "True":
    RESTART_POINTS_WEEK_DAY = timezone.now().weekday()

# Get current week day
today = timezone.now().weekday()

# validate week date
if today == RESTART_POINTS_WEEK_DAY:    
    
    # Get and loop all users to update ranking
    users = User.objects.all()
    for user in users:
        
        # Get user week points
        week_points = WeeklyPoint.objects.filter(general_point__user=user).count ()
        
        # Found new ranking
        for ranking in rankings:
            if week_points >= ranking.points:
                user.ranking = ranking
        
                # Save user ranking and end loop
                user.save()
                break
        
        # Show status
        logger.info (f"Ranking updated: user: {user}, week points: {week_points}, ranking: {user.ranking}")
            
    # Delete week points
    WeeklyPoint.objects.all().delete()
    print ("week points deleted")
        
# delete all daily points
DailyPoint.objects.all().delete()
print ("today points deleted")