# Conver today general points with amount in 0, to weekly points with amount in 1, and save them as week points

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
from django.utils import timezone
from app import models
from app.logs import logger

# Get today general points with amount in 0
now = timezone.now ()
time_start = now.replace (hour=0, minute=0, second=0, microsecond=0)
time_end = now.replace (hour=23, minute=59, second=59, microsecond=999999)
general_points = models.GeneralPoint.objects.filter (datetime__range=(time_start, time_end), amount=0)

counter = 0
for general_point in general_points:
    
    counter += 1    
    logger.info (f"Point {counter} of {len(general_points)}")
    
    # Set amount to 1
    general_point.amount = 1
    general_point.save ()
    
    # Create weekly point
    models.WeeklyPoint (general_point=general_point).save()