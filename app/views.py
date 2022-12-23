import os
from . import twitch
from . import models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv

load_dotenv ()

# Get credentials
TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_SECRET = os.environ.get("TWITCH_SECRET")
HOST = os.environ.get("HOST")

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
        print (user_token, refresh_token)
        
        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token) 
        print (user_id, user_email, user_picture, user_name)
    
        # Validate user data
        if user_id and user_email and user_picture and user_name:
            
            # Save user data in database
            new_user = models.User(user_id, user_email, user_picture, user_name, user_token, refresh_token)
            new_user.save ()
            
            # Save user data in session
            request.session["user_id"] = new_user.id
            
        else:
            # Araise error when user data is not valid
            error = True
            print ("Error al obtener datos de usuario")
        
    else:
        # Araise error where there it nor a login code
        error = True        
        print ("Error al obtener codigo de login")
    
    if error:
        # Save login error in session
        request.session["error"] = "Error al iniciar sesión con twitch. Intente de nuevo mas tarde."
        
    # Redirect to home page
    return redirect('home')
    
def home (request):
    """ Home page wqith link for login with twitch """
    
    error = ""
    
    if "error" in request.session:
        # Get error from session
        error = request.session["error"]
        del request.session["error"]
    
    # Show home or register page after login
    if "user_id" in request.session:
        
        # Get user data from cookies
        user_id = request.session["user_id"]
        user = models.User.objects.filter(id=user_id).first()
        
        # Validate if user data is completed
        if user.first_name:
            # Render home page with user data
            return render (request, 'app/home.html', user)
        else:
            # Redirect to register page
            return redirect ('register')
        
    # Show fanding if user if not logger
    else:
        
        # Redirect path for login botton
        redirect_path = f"{HOST}/login/"
        
        # Generate tiwtch login url
        twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, redirect_path)
        
        # Render page with twitch link and error message (is exist)
        return render (request, 'app/landing.html', {
            "twitch_link":  twitch_link,
            "error": error
        })
        
def register (request):
        
    # Redirect to home if user it not in session
    if not "user_id" in request.session:
        return redirect ("home")
       
    # Get user from cookie id
    user_id = request.session["user_id"]        
    user = models.User.objects.filter(id=user_id).first()
    
    # Redirect to home if user id is not valid
    if not user: 
        return redirect ("home")
    
    #  Return template with user data
    return render (request, 'app/register.html', {
        "id": user.id,
        "email": user.email,
        "picture": user.picture,
        "user_name": user.user_name
    })
        