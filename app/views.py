import os
import json
import datetime
import requests as req
from . import twitch
from . import models
from . import decorators
from . import tools
from .logs import logger
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

# Get credentials
TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_SECRET = os.environ.get("TWITCH_SECRET")
HOST = os.environ.get("HOST")
NODE_API = os.environ.get("NODE_API")

# Create your views here.
def login(request):
    """ Manage login with twitch """

    error = False
    current_path = f"{HOST}{request.path}"

    # Try to get login code from twitch, after login
    login_code = request.GET.get("code", "")

    # Detect error in login
    if login_code:
        # Get twitch token for get user data
        user_token, refresh_token = twitch.get_tokens(
            TWITCH_CLIENT_ID, TWITCH_SECRET, login_code, current_path)

        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(
            user_token)

        # Validate user data
        if user_id and user_email and user_picture and user_name:

            # Validate if user exist in database
            new_user = models.User.objects.filter(id=user_id).first()
            if not new_user:

                # Save new user data in database
                new_user = models.User(
                    user_id, user_email, user_picture, user_name, user_token, refresh_token)
                new_user.save()

            # Save user id in session
            request.session["user_id"] = new_user.id

        else:
            # Araise error when user data is not valid
            error = True
            logger.error("Error al obtener datos de usuario")

    else:
        # Araise error where there it nor a login code
        error = True
        logger.error("Error al obtener codigo de login")

    if error:
        # Save login error in session
        request.session["error"] = "Error al iniciar sesión con twitch. Intente de nuevo mas tarde."

    # Redirect to home page
    return redirect('home')


def landing(request):
    """ landing page, for not logged users """

    # Get error from session
    error = request.session.get("error", "")
    if error:
        del request.session["error"]

    # Redirect path for login botton
    redirect_path = f"{HOST}/login/"

    # Generate tiwtch login url
    twitch_link = twitch.get_twitch_login_link(TWITCH_CLIENT_ID, redirect_path)

    # Render page with twitch link and error message (is exist)
    return render(request, 'app/landing.html', {
        "twitch_link":  twitch_link,
        "error": error
    })


@decorators.validate_login
def home(request):
    """ Home page with link for login with twitch """

    # Get message from cookies
    message = request.session.get("message", "")
    if message:
        del request.session["message"]

    # Get user data from cookies
    user_id = request.session["user_id"]
    user = models.User.objects.filter(id=user_id).first()

    # Return to landing page if user id not exist in database
    if not user:
        del request.session["user_id"]
        return redirect('landing')

    # Send user to register page if user data is not complete
    if not user.first_name or user.first_name.strip() == "":
        return redirect('register')

    # Show to user to whastapp page if user is not active
    if not user.is_active:
        return render(request, 'app/whatsapp.html')

    # Render home page with user data
    return render(request, 'app/home.html', {
        "name": user.user_name,
        "message": message
    })


@decorators.validate_login
def register(request):
    """ Page for complete register, after login with twitcyh the first time """

    # Get user from cookie id
    user_id = request.session["user_id"]
    user = models.User.objects.filter(id=user_id).first()

    # Redirect to home if user id is not valid
    if not user or (user.first_name and user.first_name.strip() != ""):
        return redirect("home")

    # Retrurn template in get method with user data
    if request.method == "GET":
        return render(request, 'app/register.html', {
            "id": user.id,
            "email": user.email,
            "picture": user.picture,
            "user_name": user.user_name,
        })

    elif request.method == "POST":

        # Get user data from form
        first_name = request.POST.get("first-name", "")
        last_name = request.POST.get("last-name", "")
        country = request.POST.get("country", "")
        time_zone = request.POST.get("time-zone", "")
        phone = request.POST.get("full-phone", "")

        if not first_name or not last_name or not country or not time_zone or not phone:
            # Show error if data is not valid
            return render(request, 'app/register.html', {
                "id": user.id,
                "email": user.email,
                "picture": user.picture,
                "user_name": user.user_name,
                "error": "Algo salió mal, intente de nuevo"
            })

        # Create country and time zone objects
        country_obj = models.Country.objects.filter(country=country).first()
        time_zone_obj = models.TimeZone.objects.filter(
            time_zone=time_zone).first()
        if not country_obj:
            country_obj = models.Country(country=country)
            country_obj.save()
        if not time_zone_obj:
            time_zone_obj = models.TimeZone(time_zone=time_zone)
            time_zone_obj.save()

        # Update user data
        user.first_name = first_name
        user.last_name = last_name
        user.country = country_obj
        user.time_zone = time_zone_obj
        user.phone = phone
        user.save()

        # Save message for show in home page
        request.session["message"] = "Registro completado con éxito"

        return redirect("home")


def error404(request, exception):
    return render(request, 'app/404.html')


def logout(request):
    """ Logout user """

    # Delete user id from cookies
    if "user_id" in request.session:
        del request.session["user_id"]

    # Redirect to home
    return redirect("home")


def apoyar(request):
    """ Get data of the stream that is currently being broadcast, for node.js api"""

    # TODO: Validate if node server its running
    is_node_working = tools.is_node_working(NODE_API)

    # Render template with error message if node.js api is not working
    if is_node_working:
        return render(request, 'app/apoyar.html', {})
    else:
        return render(request, 'app/apoyar.html', {
            "error": "El bot no está disponible en este momento (tus puntos no serán contabilizados)"
        })


@csrf_exempt
def add_comment(request):
    """ Add comment to stream """

    # Get data from request
    json_data = json.loads(request.body)
    stream_id = json_data.get("stream_id", "")
    user_id = json_data.get("user_id", "")
    comment = json_data.get("comment", "")

    if not user_id or not stream_id or not comment:
        return HttpResponseBadRequest("stream_id, user_id and comment are required")

    # Get stream
    stream = models.Stream.objects.filter(id=stream_id).first()

    # Get user
    user = models.User.objects.filter(id=user_id).first()

    if not user or not stream:
        return HttpResponseBadRequest("stream id or user id is not valid")

    # Create comment
    comment_obj = models.Comment(stream=stream, comment=comment, user=user)
    comment_obj.save()

    return JsonResponse({
        "success": True
    })


@csrf_exempt
def refresh_token(request):
    """ Update access token of user, from node.js api """

    # Get data from request
    json_data = json.loads(request.body)
    expired_token = json_data.get("expired_token", "")

    if not expired_token:
        return HttpResponseBadRequest("expired_token is required")

    # Find user with expired token
    find_user = models.User.objects.filter(access_token=expired_token).first()
    if not find_user:
        return HttpResponseBadRequest("expired_token is not valid")

    new_access_token = twitch.get_new_user_token(
        TWITCH_CLIENT_ID, TWITCH_SECRET, find_user.refresh_token)
    if not new_access_token:
        return HttpResponseBadRequest("error generating new token")

    # Update user token
    find_user.access_token = new_access_token
    find_user.save()

    # Submit again data to node.js api
    tools.submit_streams_node_bg(NODE_API)

    return JsonResponse({
        "success": True
    })
