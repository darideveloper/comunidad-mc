import json
import requests
import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv, dotenv_values

# Get credentials
config = dotenv_values(".env")
TWITCH_CLIENT_ID = config["TWITCH_CLIENT_ID"]
TWITCH_SECRET = config["TWITCH_SECRET"]
HOST = config["HOST"]

# Create your views here.
def login (request):
    
    current_path = f"{HOST}{request.path}"
    
    # Get twitch token
    token_url = "https://id.twitch.tv/oauth2/token"
    res = requests.post (token_url, data={
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_SECRET,
        "grant_type": "client_credentials"
    })
    json_data = json.loads (res.content)
    token = json_data["access_token"]

    # Generate tiwtch login url
    url_params = {
        "response_type": token,
        "client_id": TWITCH_CLIENT_ID,
        "redirect_uri": current_path,
        "response_type": "code",
        "scope": "analytics:read:games bits:read channel:read:goals channel:read:polls channel:read:predictions channel:read:stream_key channel:read:subscriptions channel:read:vips moderation:read user:read:broadcast user:read:email user:read:follows user:read:subscriptions",
    }
    encoded_params = "&".join([f"{param_key}={param_value}" for param_key, param_value in url_params.items()])
    twitch_link = f"https://id.twitch.tv/oauth2/authorize?{encoded_params}"
        
    return render (request, 'app/login.html', {
        "twitch_link":  twitch_link
    })
    
def index (request):
    return render (request, 'app/index.html')
    # return HttpResponse (request)
    