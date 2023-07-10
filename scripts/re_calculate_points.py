""" Set points to the users, in old streams """

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
from app import models

prefix = "Script"

# Submit data to nodejs api, for start reading chat
twitch = TwitchApi (prefix)

# Get streams
streams = models.Stream.objects.filter (id__in=[3299, 3323])

# Delete streams points
points = models.GeneralPoint.objects.filter (stream__in=streams)
points.delete ()

# Calculate points
twitch.calculate_points(streams)