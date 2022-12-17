from django.shortcuts import render
from django.http import HttpResponse

# Get credentials
from dotenv import load_dotenv, dotenv_values
config = dotenv_values(".env")
TWITCH_CLIENT_ID = config["TWITCH_CLIENT_ID"]
TWITCH_SECRET = config["TWITCH_SECRET"]

# Create your views here.
def login (request):
    
    # Generate twitch login url
    twitch_link = f"https://id.twitch.tv/oauth2/authorize"
    twitch_link += f"?response_type=code"
    twitch_link += f"&client_id={TWITCH_CLIENT_ID}"
    twitch_link += f"&redirect_uri=http://localhost:8000"
    twitch_link += f"&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls"
    twitch_link += f"&state=c3ab8aa609ea11e793ae92361f002671"
    
    context = {
        "twitch_link":  twitch_link
    }
        
    return render (request, 'app/login.html', context)
    
def index (request):
    return render (request, 'app/index.html')
    