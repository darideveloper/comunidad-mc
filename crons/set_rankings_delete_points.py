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
from app.models import User, Ranking, WeeklyPoint, DailyPoint, PointsHistory, GeneralPoint
from app.logs import logger

# Get ranbkings and required points
rankings = Ranking.objects.all().order_by("points").reverse()

# Load environment variables
load_dotenv ()
RESTART_POINTS_WEEK_DAY = int(os.getenv('RESTART_POINTS_WEEK_DAY'))
DEBUG = os.getenv('DEBUG')
RANKING_FIRST_BITS = int(os.getenv('RANKING_FIRST_BITS'))
RANKING_SECOND_BITS = int(os.getenv('RANKING_SECOND_BITS'))
RANKING_THIRD_BITS = int(os.getenv('RANKING_THIRD_BITS'))

# Overwrite restart date in debug mode
if DEBUG == "True":
    RESTART_POINTS_WEEK_DAY = timezone.now().weekday()

# Get current week day
today = timezone.now().weekday()

# Delete points history
PointsHistory.objects.all().delete()

# validate week date
if today == RESTART_POINTS_WEEK_DAY:    
        
    # Get and loop all users to update ranking
    users = User.objects.all()
    for user in users:
        
        # Get user week points
        week_points = WeeklyPoint.objects.filter(general_point__user=user).count ()
        general_points = GeneralPoint.objects.filter(user=user).count ()
        
        # Set dimond ranking to admins
        if user.is_admin:
            user.ranking = rankings.first()
        else:
            # Found new ranking
            for ranking in rankings:
                if week_points >= ranking.points:
                    user.ranking = ranking
                    break
        
        # Save user ranking
        user.save()
        
        # Save pouints history
        PointsHistory (user=user, general_points=general_points, week_points=week_points).save()
        
        # Show status
        logger.info (f"Ranking updated: user: {user}, week points: {week_points}, ranking: {user.ranking}")
    
    # Only keep first 10 points history registers
    point_history_firsts = [point_history.id for point_history in PointsHistory.objects.all().order_by("week_points").reverse()]
    PointsHistory.objects.all().exclude(id__in=point_history_firsts[:10]).delete()
    print ("history points saved")
    
    # Delete all points
    GeneralPoint.objects.all().delete()
    print ("all points deleted")
    
else:        
    # delete all daily points
    DailyPoint.objects.all().delete()
    print ("today points deleted")