from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dotenv import load_dotenv, dotenv_values
from . import twitch

# Get credentials
config = dotenv_values(".env")
TWITCH_CLIENT_ID = config["TWITCH_CLIENT_ID"]
TWITCH_SECRET = config["TWITCH_SECRET"]
HOST = config["HOST"]

# Create your views here.
def login (request):
    """ Manage login with twitch """
    
    current_path = f"{HOST}{request.path}"
    
    # Try to get login code from twitch, after login
    login_code = request.GET.get("code", "")    
    
    if login_code: 
        # Get twitch token for get user data
        user_token, refresh_token = twitch.get_tokens(TWITCH_CLIENT_ID, TWITCH_SECRET, login_code, current_path)
            
        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token) 
        print ()
        print (user_id, user_email, user_picture, user_name)      
        
        
        # Redirect to home page
        # return redirect('index')
        return HttpResponse(f"done")

    # Generate tiwtch login url
    twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, current_path)
        
    return render (request, 'app/login.html', {
        "twitch_link":  twitch_link
    })
    
def index (request):
    return render (request, 'app/index.html')
    # return HttpResponse (request)
    