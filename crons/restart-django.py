""" Stop dynos (and auto restart) from heroku current project """

# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from dotenv import load_dotenv

load_dotenv ()

logs_origin = models.LogOrigin.objects.get (name="Restart Django")
HEROKU_TOKEN = os.getenv("HEROKU_TOKEN")
try:
    import requests

    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {HEROKU_TOKEN}"
    }

    res = requests.delete ("https://api.heroku.com/apps/comunidadmc/dynos", headers=headers)
    res_json = res.json()


    if res.status_code == 202:
        models.Log.objects.create (
            origin=logs_origin,
            log_type=models.LogType.objects.get (name="info"),
            details=f"Restarting django"
        )
    else: 
        models.Log.objects.create (
            origin=logs_origin,
            log_type=models.LogType.objects.get (name="error"),
            details=f"Restarting django error with token {HEROKU_TOKEN}: {res_json}"
        )
except Exception as e:
    models.Log.objects.create (
        origin=logs_origin,
        log_type=models.LogType.objects.get (name="error"),
        details=f"Restarting django unknown error with token {HEROKU_TOKEN}: {e}"
    )