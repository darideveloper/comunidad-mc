""" Set points to the users in the current streams """

# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.twitch import TwitchApi

# Submit data to nodejs api, for start reading chat
twitch = TwitchApi (logs_prefix="calculate points -")
twitch.calculate_points()