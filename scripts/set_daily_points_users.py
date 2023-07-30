# Set specific amount of daly points to specific users

# UPDATE THIS:
STREAMS_IDS = [4094]
POINTS = 10
USERS = ["darideveloper"]
FORCE = True

# Add parent folder to path
import os
import sys
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from app.twitch import TwitchApi

# Instance twitch api
twitch_api = TwitchApi ("Script")

# Get users
users = models.User.objects.filter(user_name__in=USERS)

# Get stream
stream = models.Stream.objects.filter(id__in=STREAMS_IDS).first()

for user in users:

    # add 10 points today
    for _ in range (POINTS):
        twitch_api.add_point(user, stream, force=FORCE)
