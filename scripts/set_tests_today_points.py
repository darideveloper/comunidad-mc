# Add parent folder to path
import os
import sys
import pytz
from django.utils import timezone
from datetime import datetime
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from app.twitch import TwitchApi

# Load environment variables
load_dotenv ()
DAY_POINTS = int(os.getenv('SCRIPTS_DAY_POINTS'))
USER_NAME = os.getenv('SCRIPTS_USER_NAME')

# Get user instance and last stream
user = models.User.objects.filter(user_name=USER_NAME).first()
stream = models.Stream.objects.all().order_by('datetime').last()

# Delete user from ranking
models.TopDailyPoint.objects.filter (user=user).delete()

# Loop for save each user point
twitch_api = TwitchApi ()
for _ in range (DAY_POINTS):
    twitch_api.add_point_bg(user, stream, 2)
    print ()
    
