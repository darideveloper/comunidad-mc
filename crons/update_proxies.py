# Add parent folder to path
import os
import sys
from time import sleep
from django.utils import timezone
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app.logs import logger
from botviews import models as views_models
from botcheers import models as cheers_models

import requests
from dotenv import load_dotenv

# Environment variables
load_dotenv ()
API_TOKEN_PROXIES = os.getenv ('API_TOKEN_PROXIES')

logs_prefix = "update_proxies -"

# Get proxies
res = requests.get (
    "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100", 
    headers = { 
        "Authorization": f"Token {API_TOKEN_PROXIES}"
    }
)
if res.status_code != 200:
    logger.error (f"{logs_prefix} Error getting proxies: {res.status_code} - {res.text}")
    sys.exit (1)

try:
    json_data = res.json ()
    proxies = json_data['results']
except Exception as e:
    logger.error (f"{logs_prefix} Error getting proxies: {e}")
    sys.exit (1)

# Delete old proxies
views_models.Proxy.objects.all().delete()
cheers_models.Proxy.objects.all().delete()
logger.info (f"{logs_prefix} Old proxies deleted")

# Save each proxy in database
for proxy in proxies:
    
    if not proxy:
        continue
    
    views_models.Proxy.objects.create(
        host=proxy["proxy_address"],
        port=proxy["port"],
        user=proxy["username"],
        password=proxy["password"],
    )
    
    cheers_models.Proxy.objects.create(
        host=proxy["proxy_address"],
        port=proxy["port"],
    )
    
    logger.info (f"{logs_prefix} {proxy['id']} saved")

# SHow proxies counter
logger.info (f"{logs_prefix} {len(proxies)} proxies saved")

print ()