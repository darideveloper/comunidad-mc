""" Check points of users and set ranking, and delete old points """

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
from app import tools
from django.utils import timezone
from app.models import User, Ranking, WeeklyPoint, DailyPoint, \
    PointsHistory, GeneralPoint, Bits, TopDailyPoint, StreamExtra, StreamVip
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

# validate week date
if today == RESTART_POINTS_WEEK_DAY:    
    
    # Delete points history for global ranking
    PointsHistory.objects.all().delete()
    
    # Delete extra streams
    StreamExtra.objects.all().delete()
    
    # Delete vips
    StreamVip.objects.all().delete()
        
    # Get and loop all users to update ranking
    users = User.objects.all()
    for user in users:
        
        # Get user week points
        *other, general_points_num, weekly_points_num, _ = tools.get_user_points (user)
        
        # Set ranking to admins
        admin_type = tools.get_admin_type (user)
        if admin_type:
            ranking = user.admin_type.ranking
        else:
            # Found new ranking
            for ranking in rankings:
                if weekly_points_num >= ranking.points:
                    user.ranking = ranking
                    break
                
        user.ranking = ranking
        
        # Save user ranking
        user.save()
        
        # Save pouints history
        PointsHistory (user=user, general_points=general_points_num, week_points=general_points_num).save()
        
        # Show status
        logger.info (f"Ranking updated: user: {user}, week points: {weekly_points_num}, ranking: {user.ranking}")
    
    # Add bits to first, second and third users in points table
    points_history_all = PointsHistory.objects.all().order_by("general_points").reverse()
    print (points_history_all)
    first_user = points_history_all[0].user
    second_user = points_history_all[1].user
    third_user = points_history_all[2].user
    Bits (user=first_user, amount=RANKING_FIRST_BITS).save ()
    Bits (user=second_user, amount=RANKING_SECOND_BITS).save ()
    Bits (user=third_user, amount=RANKING_THIRD_BITS).save ()
    print ("Bits added to first, second and third users")
    
    # Add a vip to first user
    StreamVip (user=first_user).save ()
    print ("Vips added to first user")
    
    # Delete top daily points
    TopDailyPoint.objects.all().delete()
    print ("top daily points deleted")
    
    # Delete week points
    WeeklyPoint.objects.all().delete()
    print ("week points deleted")
    
    # Delete all points
    GeneralPoint.objects.all().delete()
    print ("all points deleted")
    
else:        
    # delete all daily points
    DailyPoint.objects.all().delete()
    print ("today points deleted")