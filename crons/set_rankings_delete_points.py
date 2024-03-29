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
from django.utils import timezone

load_dotenv ()

log_origin_name = "Set Ranking Delete Points"
try:
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)

    # Get ranbkings and required points
    rankings = models.Ranking.objects.all().order_by("points").reverse()

    # Load environment variables
    RESTART_POINTS_WEEK_DAY = int(os.getenv('RESTART_POINTS_WEEK_DAY'))
    RESTART_DAY = False
    RANKING_FIRST_BITS = int(os.getenv('RANKING_FIRST_BITS'))
    RANKING_SECOND_BITS = int(os.getenv('RANKING_SECOND_BITS'))
    RANKING_THIRD_BITS = int(os.getenv('RANKING_THIRD_BITS'))

    # Overwrite restart date in debug mode
    if RESTART_DAY:
        RESTART_POINTS_WEEK_DAY = timezone.now().weekday()

    # Get current week day
    today = timezone.now().weekday()

    # validate week date
    if today == RESTART_POINTS_WEEK_DAY:    
        
        # Delete points history for global ranking
        models.PointsHistory.objects.all().delete()
        
        # Delete old vips and frees
        models.StreamVip.objects.all().delete()
        models.StreamFree.objects.all().delete()
            
        # Get and loop all users to update ranking
        users = models.User.objects.filter (is_active=True)
        for user in users:
            
            # Get user week points
            general_points, weekly_points, daily_points, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
            
            ranking_found = None
            admin_type = tools.get_admin_type (user)
            if admin_type:
                # Found ranking to admins
                if admin_type == "admin diamante":
                    ranking_found = models.Ranking.objects.get (name="admin")
                elif admin_type == "admin platino":
                    ranking_found = models.Ranking.objects.get (name="platino")            
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
            models.PointsHistory (
                user=user, 
                general_points_num=general_points_num, 
                general_points_week_num=general_points_week_num,
                week_points_num=weekly_points_num,
            ).save()
            
            # Show status
            models.Log.objects.create ( 
                origin=log_origin,
                details=f"Ranking updated: user: {user}, week points: {weekly_points_num}, ranking: {user.ranking.name}"
            )
        
        # Add bits to first, second and third users in points table
        points_history_all = models.PointsHistory.objects.all().order_by("general_points_week_num", "general_points_num").reverse()
        first_user = points_history_all[0].user
        second_user = points_history_all[1].user
        third_user = points_history_all[2].user
        # models.Bit (user=first_user, amount=RANKING_FIRST_BITS, details="1er lugar del Ranking Semanal").save ()
        # models.Bit (user=second_user, amount=RANKING_SECOND_BITS, details="2do lugar del Ranking Semanal").save ()
        # models.Bit (user=third_user, amount=RANKING_THIRD_BITS, details="3er lugar del Ranking Semanal").save ()
        # models.Log.objects.create ( 
        #     origin=log_origin,
        #     details=f"Bits added to first, second and third users ({first_user}, {second_user}, {third_user}))"
        # )
        
        # Add vip and extra stream to fiset user
        models.StreamVip (user=first_user).save ()
        models.StreamExtra (user=first_user).save ()
        models.Log.objects.create ( 
            origin=log_origin,
            details=f"vip and free added to first user {first_user}"
        )
        
        # Add a free and a extra to second user
        models.StreamFree (user=second_user).save ()
        models.StreamExtra (user=second_user).save ()
        models.Log.objects.create ( 
            origin=log_origin,
            details=f"extra and free added to second user {second_user}"
        )
        
        # backuop weekly points
        models.WeeklyPointBackup.objects.all().delete()
        models.Log.objects.create ( 
            origin=log_origin,
            details=f"weekly points backup deleted"
        )
        weekly_points = models.WeeklyPoint.objects.all()
        for weekly_point in weekly_points:
            models.WeeklyPointBackup (general_point=weekly_point.general_point).save()
        models.Log.objects.create ( 
            origin=log_origin,
            details=f"weekly points backup created"
        )
        
        # Delete week points
        models.WeeklyPoint.objects.all().delete()
        models.Log.objects.create ( 
            origin=log_origin,
            details=f"week points deleted"
        )

    # delete all daily points
    models.DailyPoint.objects.all().delete()
    models.Log.objects.create ( 
        origin=log_origin,
        details=f"today points deleted"
    )

    # delete top daily points
    models.TopDailyPoint.objects.all().delete()
    models.Log.objects.create ( 
        origin=log_origin,
        details=f"top points deleted"
    )
except Exception as e:
    
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )
    