import os
import json
import pytz
import datetime
import requests as req
from .twitch import TwitchApi
from . import models
from . import decorators
from .logs import logger
from .tools import get_user_message_cookies, get_user_points
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

# Get credentials
load_dotenv()
HOST = os.environ.get("HOST")

# Twitch instance
twitch = TwitchApi ()

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
        user_token, refresh_token = twitch.get_tokens(login_code, current_path)

        # Get user data
        user_id, user_email, user_picture, user_name = twitch.get_user_info(user_token)

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
    twitch_link = twitch.get_twitch_login_link(redirect_path)

    # Render page with twitch link and error message (is exist)
    return render(request, 'app/landing.html', {
        "twitch_link":  twitch_link,
        "error": error,
        "current_page": "landing"
    })


@decorators.validate_login
def home(request):
    """ Home page with link for login with twitch """

    user, message = get_user_message_cookies(request)

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

    # Redirect to Apoyar page
    return redirect("support")

@decorators.validate_login
def register(request):
    """ Page for complete register, after login with twitcyh the first time """

    # Get user from cookies
    user, _ = get_user_message_cookies(request)

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
    is_node_working = twitch.is_node_working(NODE_API)

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
    logger.info (f"Comment added: {comment_obj.id}")
    
    # Try to add point to user
    twitch.add_point(user)

    return JsonResponse({
        "success": True
    })


@csrf_exempt
def refresh_token(request):
    """ Update access token of user, from node.js api """

    # Get data from request
    json_data = json.loads(request.body)
    stream_id = json_data.get("stream_id", "")
    if not stream_id:
        return HttpResponseBadRequest("stream_id is required")

    # Find user with expired token
    find_stream = models.Stream.objects.filter(id=stream_id).first()
    if not find_stream:
        return HttpResponseBadRequest("stream_id is not valid")
    find_user = id=find_stream.user

    token_updated = twitch.update_token(find_user)
    if not token_updated:
        return HttpResponseBadRequest("error updateding token")

    # Submit again data to node.js api
    twitch.submit_streams_node_bg()    
    return JsonResponse({
        "success": True
    })
    
@decorators.validate_login
def points(request):
    """ Page for show the points of the user """
    
    # Get user data
    user, message = get_user_message_cookies(request)
    profile_image = user.picture
    general_points, weekly_points, daily_points = get_user_points (user)
    
    # Get only last 60 points
    general_points_table = general_points
    if general_points_table.count() > 20:
        general_points_table = general_points_table[:20]
        
    # Get user time zone
    user_time_zone = user.time_zone.time_zone
            
    # Format table points
    points_data = []
    current_points = general_points.count()
    for point in daily_points:
        
        # Calculate datetime with time zone of the user
        datetime_user = point.general_point.datetime.astimezone(pytz.timezone(user_time_zone))
        date = datetime_user.strftime("%d/%m/%Y")
        time = datetime_user.strftime("%I:%M %p")
        channel = point.general_point.stream.user.user_name
        
        points_data.append ({
            "date": date,
            "time": time,
            "my_points": current_points,
            "channel": channel
        })

        # Decress punits counter
        current_points -= 1
        
    # Render page
    return render(request, 'app/points.html', {
        # General context
        "name": user.user_name,
        "message": message,
        
        # User profile context
        "current_page": "points",
        "profile_image": profile_image,
        "general_points_num": general_points.count(),
        "weekly_points_num": weekly_points.count(),
        "daily_points_num": daily_points.count(),
        "ranking": user.ranking.name,
        "profile_card_layout": "vertical",
        
        # Specific context
        "points": points_data,
    })

@decorators.validate_login
def schedule(request):
    """ Page for schedule stream """
    
    # Get user data
    user, message = get_user_message_cookies(request)
    profile_image = user.picture
    general_points, weekly_points, daily_points = get_user_points (user)
    
    # Render page
    return render(request, 'app/schedule.html', {
        # General context
        "name": user.user_name,
        "message": message,
        
        # User profile context
        "current_page": "schedule",
        "profile_image": profile_image,
        "general_points_num": general_points.count(),
        "weekly_points_num": weekly_points.count(),
        "daily_points_num": daily_points.count(),
        "ranking": user.ranking.name,
        "profile_card_layout": "horizontal",
        
        # Specific context
    })
    
@decorators.validate_login
def support(request):
    """ Page for show live streamers and copy link to stream """
    
    user, message = get_user_message_cookies(request)

    # Render page
    return render(request, 'app/support.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "support"
    })
    
@decorators.validate_login
def ranking(request):
    """ Page for show the live ranking of the users based in points """
    
    # Get user data
    user, message = get_user_message_cookies(request)
    profile_image = user.picture
    general_points, weekly_points, daily_points = get_user_points (user)
    
    # Get top 10 users from TopDailyPoint
    ranking_today = [[register.position, register.user.user_name] for register in models.TopDailyPoint.objects.all()]
    
    # Get top 10 users from general points
    points_history = models.PointsHistory.objects.all().order_by("general_points").reverse()[:10]
    ranking_global = [[index + 1, register.user.user_name, register.general_points, f'app/imgs/icon_{register.user.ranking}.png', register.user.picture, register.user.ranking] \
        for index, register in enumerate(points_history)]
    ranking_global_top = ranking_global[:3]
    ranking_global_other = ranking_global[3:]
    
    # Render page
    return render(request, 'app/ranking.html', {
        # General context
        "name": user.user_name,
        "message": message,
        
        # User profile context
        "current_page": "ranking",
        "profile_image": profile_image,
        "general_points_num": general_points.count(),
        "weekly_points_num": weekly_points.count(),
        "daily_points_num": daily_points.count(),
        "ranking": user.ranking.name,
        "profile_card_layout": "horizontal small",
        
        # Specific context
        "ranking_today": ranking_today,
        "ranking_global_top": ranking_global_top,
        "ranking_global_other": ranking_global_other,
    })
    
@decorators.validate_login
def profile(request):
    """ Page for show and update the user data """
    
    user, message = get_user_message_cookies(request)

    # Render page
    return render(request, 'app/profile.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "profile"
    })
    
@decorators.validate_login
def wallet(request):
    """ Page for withdraw bits to wallet """
    
    user, message = get_user_message_cookies(request)

    # Render page
    return render(request, 'app/wallet.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "wallet"
    })