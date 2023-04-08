# Set specific points to all users, in current stream

# Add parent folder to path
import os
import sys
import random
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from app.twitch import TwitchApi

users = models.User.objects.all()

# Connect to twitch class
twitch_api = TwitchApi ()

stream = twitch_api.get_current_streams ()[0]

# Loop users for add points
for user_name in users: 
    
    # Get user
    user = models.User.objects.filter(user_name=user_name).first()
    
    # Skip if user not found
    if not user:
        continue
    
    # add 10 points today
    for _ in range (1):
        twitch_api.add_cero_point (user, stream)
        twitch_api.add_point(user, stream, force=True)
    