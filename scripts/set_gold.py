# set gold ranking to users who have specific amount of weekly points

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

# Get ranbkings and required points
rankings = models.Ranking.objects.all().order_by("points").reverse()
gold_points = 45
gold_ranking = models.Ranking.objects.get (name="oro")

# Get and loop all users to update ranking
users = models.User.objects.all()
for user in users:
    
    # Get user week points
    general_points, weekly_points, daily_points, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
    
    if weekly_points_num >= gold_points:  
        # Update ranking    
        user.ranking = gold_ranking  
        user.save()
    
        print (f"User {user}, points: {weekly_points_num}, now is gold")
    else:
        print (f"User {user}, points: {weekly_points_num}, no gold")