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
        
        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token) 
    
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

def landing (request):
    """ landing page, for not logged users """
        
    # Get error from session
    error = request.session.get ("error", "")
    if error:
        del request.session["error"]
    
    # Redirect path for login botton
    redirect_path = f"{HOST}/login/"
    
    # Generate tiwtch login url
    twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, redirect_path)
    
    # Render page with twitch link and error message (is exist)
    return render (request, 'app/landing.html', {
        "twitch_link":  twitch_link,
        "error": error
    })

def home (request):
    """ Home page with link for login with twitch """
    
    # Get message from cookies
    message = request.session.get("message", "")
    if message:
        del request.session["message"]
    
    # Show home or register page after login
    if "user_id" in request.session:
        
        # Get user data from cookies
        user_id = request.session["user_id"]
        user = models.User.objects.filter(id=user_id).first()
        
        # Return to landing page if user id not exist in database
        if not user:
            del request.session["user_id"]
            return redirect ('landing')
        
        # Validate if user data is completed
        if user.first_name and user.first_name.strip() != "":
            # Render home page with user data
            return render (request, 'app/home.html', {
                "name": user.user_name,
                "message": message
            })
        else:
            # Redirect to register page
            return redirect ('register')
        
    # Show fanding if user if not logger
    else:
        return redirect ('landing')
        
def register (request):
    """ Page for complete register, after login with twitcyh the first time """
        
    # Redirect to home if user it not in session
    if not "user_id" in request.session:
        return redirect ("home")
       
    # Get user from cookie id
    user_id = request.session["user_id"]        
    user = models.User.objects.filter(id=user_id).first()
        
    # Redirect to home if user id is not valid
    if not user or (user.first_name and user.first_name.strip() != ""): 
        return redirect ("home")
    
    # Retrurn template in get method with user data
    if request.method == "GET":
        return render (request, 'app/register.html', {
            "id": user.id,
            "email": user.email,
            "picture": user.picture,
            "user_name": user.user_name,
        })
        
    elif request.method == "POST":
        
        # Get user data from form
        first_name = request.POST.get ("first-name", "")
        last_name = request.POST.get ("last-name", "")
        country = request.POST.get ("country", "")
        time_zone = request.POST.get ("time-zone", "")
        phone = request.POST.get ("full-phone", "")
        
        if not first_name or not last_name or not country or not time_zone or not phone:
            # Show error if data is not valid
            return render (request, 'app/register.html', {
            "id": user.id,
            "email": user.email,
            "picture": user.picture,
            "user_name": user.user_name,
            "error": "Algo salió mal, intente de nuevo"
        })
        
        # Updsate user data
        user.first_name = first_name
        user.last_name = last_name
        user.country = country
        user.time_zone = time_zone
        user.phone = phone
        user.save ()
        
        # Save message for show in home page
        request.session["message"] = "Registro completado con éxito"
        
        return redirect ("home")

def error404 (request, exception):
    return render (request, 'app/404.html')