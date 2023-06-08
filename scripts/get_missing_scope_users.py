# Test to get checks from all users
import requests

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
from app.logs import logger

twitch = TwitchApi ()

users = models.User.objects.all()

error_users = []
for user in users:
    
    # Loop for update token if is invalid
    for _ in range (2):

        user_id = user.id
        user_token = user.access_token
        url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Client-Id": "p1yxg1ystvc7ikxem39q7mhqq9fk59" # twitch client id from .env
        }
        res = requests.get(url, headers=headers)
        json_data = res.json()
        
        if "data" in json_data:
            break
        
        # Auto update user token
        if "message" in json_data:
            message = json_data["message"]
            logger.info (f"user {user}: {message}")
            if message == "Invalid OAuth token":
                twitch.update_token (user)
                continue
            else:
                logger.error (f"user {user}: {message}")