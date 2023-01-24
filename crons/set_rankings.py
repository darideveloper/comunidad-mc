# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.models import User, Ranking, WeeklyPoint
from app.logs import logger

# Get ranbkings and required points
rankings = Ranking.objects.all().order_by("points").reverse()

# Get and loop all users
users = User.objects.all()
for user in users:
    
    # Get user week points
    week_points = WeeklyPoint.objects.filter(general_point__user=user).count ()
    
    # Found new ranking
    for ranking in rankings:
        if week_points >= ranking.points:
            user.ranking = ranking
    
            # Save user ranking and end loop
            user.save()
            break
    
    # Show status
    logger.info (f"Ranking updated: user: {user}, week points: {week_points}, ranking: {user.ranking}")
    
    # TODO: Delete last week points
    
    
    

