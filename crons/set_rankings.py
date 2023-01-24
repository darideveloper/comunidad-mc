# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.models import User, Ranking
from app.tools import set_user_points
from app.logs import logger

# Get ranbkings and required points
rankings = Ranking.objects.all().order_by("points").reverse()

# Get and loop all users
users = User.objects.all()
for user in users:
        
    set_user_points (user)
    
    # Update points
    user.week_points = week_points
    user.total_points = total_points
    
    # Update ranking
    for ranking in rankings:
        if total_points >= ranking.points:
            user.ranking = ranking
            break
    
    # Save user new data
    user.save()
    
    # Show status
    logger.info ("Ranking updated: user: {user}, week points: {week_points}, ranking: {user.ranking}")
    
    # TODO: Delete last week points
    
    
    

