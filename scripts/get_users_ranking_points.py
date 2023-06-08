# Add specific number of general points to all users

# Add parent folder to path
import os
import sys
import random
from datetime import timedelta
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models, tools

# get all users
users = models.User.objects.all()

for user in users:
    # Get user week points
    _, _, _, _, weekly_points_num, _ = tools.get_user_points (user)
    
    # Get user ranking
    ranking = user.ranking.name
    
    print (f"{user.user_name.ljust(20)} {ranking.ljust(10)} {str(weekly_points_num).ljust(5)}")