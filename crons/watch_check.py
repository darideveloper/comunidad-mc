""" Check if users are in chat of streams """

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
twitch = TwitchApi ()
twitch.check_users_in_chat ()