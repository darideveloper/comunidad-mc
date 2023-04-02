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
from app import models
from app import tools
from app.logs import logger
from django.utils import timezone
from django.db.models import Sum

# Get ranbkings and required points
rankings = models.Ranking.objects.all().order_by("points").reverse()

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
    models.PointsHistory.objects.all().delete()
    
    # Delete extra streams
    models.StreamExtra.objects.all().delete()
    
    # Delete vips
    models.StreamVip.objects.all().delete()
        
    # Get and loop all users to update ranking
    users = models.User.objects.all()
    for user in users:
        
        # Get user week points
        general_points, weekly_points, daily_points, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
        
        ranking_found = None
        admin_type = tools.get_admin_type (user)
        if admin_type:
            # Found ranking to admins
            admin_name = admin_type.replace ("admin", "").strip()
            ranking_found = models.Ranking.objects.get (name=admin_name)
        else:
            # Found ranking to normal users
            for ranking in rankings:
                if weekly_points_num >= ranking.points:
                    ranking_found = ranking
                    break
                
        # Update ranking    
        user.ranking = ranking_found  
        user.save()
        
        general_points_week, general_points_week_num = tools.get_general_points_last_week (user)
        
        # Save pouints history
        models.PointsHistory (user=user, general_points=general_points_num, week_points=general_points_week_num).save()
        
        # Show status
        logger.info (f"Ranking updated: user: {user}, week points: {weekly_points_num}, ranking: {user.ranking.name}")
    
    # Add bits to first, second and third users in points table
    points_history_all = models.PointsHistory.objects.all().order_by("week_points").reverse()
    first_user = points_history_all[0].user
    second_user = points_history_all[1].user
    third_user = points_history_all[2].user
    models.Bit (user=first_user, amount=RANKING_FIRST_BITS, details="1er lugar del Ranking Semanal").save ()
    models.Bit (user=second_user, amount=RANKING_SECOND_BITS, details="2do lugar del Ranking Semanal").save ()
    models.Bit (user=third_user, amount=RANKING_THIRD_BITS, details="3er lugar del Ranking Semanal").save ()
    print ("Bits added to first, second and third users")
    
    # Add a vip to first user
    models.StreamVip (user=first_user).save ()
    print ("Vip added to first user")
    
    # Delete top daily points
    models.DailyPoint.objects.all().delete()
    print ("top daily points deleted")
    
    # Delete week points
    models.WeeklyPoint.objects.all().delete()
    print ("week points deleted")
    
    # Delete all points
    # models.GeneralPoint.objects.all().delete()
    # print ("all points deleted")
    
else:        
    # delete all daily points
    models.DailyPoint.objects.all().delete()
    print ("today points deleted")