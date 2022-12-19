from django.http import HttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv, dotenv_values
from . import twitch
from . import models

# Get credentials
config = dotenv_values(".env")
TWITCH_CLIENT_ID = config["TWITCH_CLIENT_ID"]
TWITCH_SECRET = config["TWITCH_SECRET"]
HOST = config["HOST"]

# Create your views here.
def login (request):
    """ Manage login with twitch """
    
    error = False
    current_path = f"{HOST}{request.path}"
    
    # Try to get login code from twitch, after login
    login_code = request.GET.get("code", "")    
    
    # Detect error in login
    if login_code:
        # Get twitch token for get user data
        user_token, refresh_token = twitch.get_tokens(TWITCH_CLIENT_ID, TWITCH_SECRET, login_code, current_path)
            
        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token) 
    
        # Validate user data
        if user_id and user_email and user_picture and user_name:
            
            # Save user data in database
            new_user = models.User(user_id, user_email, user_picture, user_name, user_token, refresh_token)
            new_user.save ()
            
            # Save user data in session
            request.session["user"] = {
                "id": new_user.id,
                "email": new_user.email,
                "picture": new_user.picture,
                "name": new_user.name,
            }
            
        else:
            # Araise error when user data is not valid
            error = True
        
    else:
        # Araise error where there it nor a login code
        error = True        
    
    if error:
        # Save login error in session
        request.session["error"] = "Error in login with twitch. Try again later."
        
    # Redirect to home page
    return redirect('index')
    
def index (request):
    """ Home page wqith link for login with twitch """
    
    # Get error from session
    error = ""
    if "error" in request.session:
        error = request.session["error"]
        del request.session["error"]
    
    redirect_path = f"{HOST}/login/"
    
    # Generate tiwtch login url
    twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, redirect_path)
            
    return render (request, 'app/index.html', {
        "twitch_link":  twitch_link,
        "error": error
    })
    