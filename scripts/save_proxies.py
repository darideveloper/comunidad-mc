# Save proxies in table "proxy" in botview app

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
from botviews import models

LOCATION = 'usa'

# paths
current_folder = os.path.dirname(__file__)
proxies_file = os.path.join(current_folder, 'proxies.txt')

# read proxies
with open(proxies_file, 'r') as file:
    proxies = file.readlines()
    
# Get location instance
location = models.Location.objects.get(name=LOCATION)

# Save each proxy in database
for proxy in proxies:
    
    proxy = proxy.strip()
    if not proxy:
        continue
     
    host, port, user, password = proxy.split(':')
    models.Proxy.objects.create(
        host=host,
        port=port,
        user=user,
        password=password,
        location=location
    )
    
    print (f"{proxy} saved")