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
from botviews import models as views_models
from botcheers import models as cheers_models

import requests
from dotenv import load_dotenv
from app import models

log_origin_name = "Update Proxies"
log_type_error = models.LogType.objects.get (name="error")
try:

    # Environment variables
    load_dotenv ()
    API_TOKEN_PROXIES = os.getenv ('API_TOKEN_PROXIES')

    log_origin = models.LogOrigin.objects.get (name=log_origin_name)

    # Get proxies
    res = requests.get (
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100", 
        headers = { 
            "Authorization": f"Token {API_TOKEN_PROXIES}"
        }
    )
    if res.status_code != 200:
        models.Log.objects.create (
            origin=log_origin,
            details=f"Error getting proxies: {res.status_code} - {res.text}",
            log_type=log_type_error,
        )
        sys.exit (1)

    try:
        json_data = res.json ()
        proxies = json_data['results']
    except Exception as e:
        models.Log.objects.create (
            origin=log_origin,
            details=f"Error getting proxies: {e}",
            log_type=log_type_error,
        )
        
        sys.exit (1)

    # Delete old proxies
    views_models.Proxy.objects.all().delete()
    cheers_models.Proxy.objects.all().delete()
    models.Log.objects.create (
        origin=log_origin,
        details=f"Old proxies deleted",
    )

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
        
        models.Log.objects.create (
            origin=log_origin,
            details=f"{log_origin} {proxy['id']} saved",
        )
        
    # SHow proxies counter
    models.Log.objects.create (
        origin=log_origin,
        details=f"{len(proxies)} proxies saved",
    )
    
except Exception as e:
    
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )