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
    
    # Try to get login code from twitch, after login
    login_code = request.GET.get("code", "")    
    
    if not login_code:
        # Save error in session
        request.session["error"] = "Error in login with twitch. Try again later."
        
        # Redirect to home page
        return redirect('index')
        
    # Get twitch token for get user data
    user_token, refresh_token = twitch.get_tokens(TWITCH_CLIENT_ID, TWITCH_SECRET, login_code, current_path)
        
    # Get user data
    user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token) 
    print ()
    print (user_id, user_email, user_picture, user_name)      
    
    
    # Redirect to home page
    return HttpResponse(f"done")
    
def index (request):
    """ Home page wqith link for login with twitch """
    
    # Get error from session
    error = ""
    if "error" in request.session:
        error = request.session["error"]
        del request.session["error"]
    
    current_path = f"{HOST}{request.path}"
    
    # Generate tiwtch login url
    twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, current_path)
            
    return render (request, 'app/index.html', {
        "twitch_link":  twitch_link,
        "error": error
    })
    