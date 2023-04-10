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
from app import models
from app.twitch import TwitchApi
from app.logs import logger

# get all users
users = models.User.objects.all()

# Connect to twitch class
twitch_api = TwitchApi ()

POINTS_NUM = 20

# Find last stream of Dari Developer
daridev = models.User.objects.get (user_name="DariDeveloper")
stream = models.Stream.objects.filter (user=daridev).order_by('datetime').reverse().first()

# Loop users for add points
for user_name in users: 
    
    # Get user
    user = models.User.objects.filter(user_name=user_name).first()
    
    # Create general point
    info_point = models.InfoPoint.objects.get (info="semana de prueba")
    general_point = models.GeneralPoint (
        user=user, 
        stream=stream, 
        datetime=timezone.now() - timedelta(hours=2), 
        info=info_point, 
        amount=20
    )
    general_point.save()
    
    # Create weekly points
    models.WeeklyPoint (general_point=general_point).save()
    
    logger.info (f"Added {POINTS_NUM} weekly points to {user.user_name}")

    