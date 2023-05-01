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

weekly_points = models.WeeklyPoint.objects.all ().delete ()

