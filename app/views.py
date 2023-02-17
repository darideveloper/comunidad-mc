import os
import json
import pytz
import datetime
from . import tools
from . import models
from . import decorators
from .twitch import TwitchApi
from .logs import logger
from collections import OrderedDict
from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Sum

# Get credentials
load_dotenv()
HOST = os.environ.get("HOST")

# Twitch instance
twitch = TwitchApi ()

WEEK_DAYS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
MONTHS = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

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

                # Get lower ranking
                lower_ranking = models.Ranking.get_lower()
                

                # Save new user data in database
                new_user = models.User()
                new_user.id = user_id
                new_user.email = user_email
                new_user.picture = user_picture
                new_user.user_name = user_name
                new_user.access_token = user_token
                new_user.refresh_token = refresh_token
                new_user.ranking = lower_ranking
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
def whatsapp (request):
    """ Page for request whatsapp validation """
    return render(request, 'app/whatsapp.html', {
        "current_page": "whatsapp",
    })

@decorators.validate_login
def home(request):
    """ Home page with link for login with twitch """

    user, *other = tools.get_cookies_data(request)

    # Return to landing page if user id not exist in database
    if not user:
        del request.session["user_id"]
        return redirect('landing')

    # Send user to register page if user data is not complete
    if not user.first_name or user.first_name.strip() == "":
        return redirect('register')

    # Show to user to whatsapppage if user is not active
    if not user.is_active:
        return redirect("whatsapp")        

    # Redirect to Apoyar page
    return redirect("support")

@decorators.validate_login_active
def register(request):
    """ Page for complete register, after login with twitcyh the first time """

    # Get user from cookies
    user, *other = tools.get_cookies_data(request)

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
            "current_page": "register"
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
                "error": "Algo salió mal, intente de nuevo",
                "current_page": "register"
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

@decorators.validate_login_active
def points(request):
    """ Page for show the points of the user """
    
    # Get user data
    user, message, _ = tools.get_cookies_data(request)
    profile_image = user.picture
    general_points, weekly_points, daily_points, \
        general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
    
    # Get only last 60 points
    general_points_table = general_points
    if general_points_table.count() > 20:
        general_points_table = general_points_table[:20]
        
    # Get user time zone
    user_time_zone = user.time_zone.time_zone
            
    # Format table points
    points_data = []
    current_points = general_points_num
    for point in general_points_table:
        
        # Calculate datetime with time zone of the user
        datetime_user = point.datetime.astimezone(pytz.timezone(user_time_zone))
        date = datetime_user.strftime("%d/%m/%Y")
        time = datetime_user.strftime("%I:%M %p")
        channel = ""
        if point.stream:
            channel = f" ({point.stream.user.user_name})"
        
        points_data.append ({
            "date": date,
            "time": time,
            "my_points": current_points,
            "points": point.amount, 
            "details": point.info.info + channel
        })
        
        # Decress punits counter
        current_points -= point.amount
        
    # Render page
    return render(request, 'app/points.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "current_page": "points",
        
        # User profile context
        "profile_image": profile_image,
        "general_points_num": general_points_num,
        "weekly_points_num": weekly_points_num,
        "daily_points_num": daily_points_num,
        "ranking": user.ranking.name,
        "profile_card_layout": "vertical",
        
        # Specific context
        "points": points_data,
    })
    
@decorators.validate_login_active
def schedule(request):
    """ Page for schedule stream """
    
    # Get user data
    user, message, error = tools.get_cookies_data(request)
    profile_image = user.picture
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
    user_time_zone = pytz.timezone(user.time_zone.time_zone)
    
    # Validate if stream can be saved, in post 
    if request.method == "POST":
        
        # Get next streams of the user in the next 7 days
        user_streams, streams = tools.get_user_streams(user, user_time_zone)
        
        user_streams_num = 0
        if user_streams:
            user_streams_num = user_streams.count()
        
        # Get stream data
        form_date = request.POST.get("date", "")
        form_hour = request.POST.get("hour", "")
        
        # Convert to datetime
        selected_datetime = datetime.datetime.strptime(form_date + " " + form_hour, "%Y-%m-%d %H")
        selected_datetime = selected_datetime.astimezone (user_time_zone)
        
        # Calculate available points
        available_points = general_points_num - user_streams_num * 50 
        
        # Infinity streams for admins
        if user.admin_type:
            max_streams = user_streams_num + 1
        
        # Validte if regular user have available streams
        else:
            max_streams = user.ranking.max_streams
            streams_extra = models.StreamExtra.objects.filter(user=user).all()
            if streams_extra.count() > 0:
                streams_extra_num = streams_extra.aggregate(Sum('amount'))['amount__sum']
                max_streams += streams_extra_num
                
            available_stream = max_streams - user_streams_num > 0
            if not available_stream or available_points < 50:
                error = f"Lo sentimos. No cuentas con ranking o puntos suficientes para agendar mas streams."
        
        # Validate if the date and time are free
        if not error:
            streams_match = models.Stream.objects.filter (datetime=selected_datetime)
            if streams_match.count() > 1:
                error = "Lo sentimos. Esa fecha y hora ya está agendada."
                
        # Schedule stream
        if not error:
            new_stream = models.Stream (user=user, datetime=selected_datetime)
            new_stream.save ()
            message = "Stream agendado!"
            
    # Get next streams of the user in the next 7 days
    user_streams, streams = tools.get_user_streams(user, user_time_zone)
        
    # Get available days of the week
    today = datetime.datetime.today().astimezone(user_time_zone)
    today_week = today.weekday()
    today_week_name = WEEK_DAYS[today_week]
    available_days = []
    for day_num in range (0, 7):
        
        # Calculate dates
        day_name = WEEK_DAYS[day_num]
        date = today + datetime.timedelta(days=day_num-today_week)
        date_text_day = date.strftime("%d")
        date_text_month = date.strftime("%B")
        date_text_month_spanish = MONTHS[date_text_month]
        date_text = f"{date_text_day} de {date_text_month_spanish}"
        date_formatted = date.strftime("%Y-%m-%d")
        
        # Date status
        disabled = False
        active = False
        if day_num == today_week:
            active = True
        elif day_num < today_week:
            disabled = True
           
        # Add date 
        available_days.append({
            "name": day_name, 
            "num": day_num, 
            "disabled": disabled, 
            "active": active, 
            "date": date_formatted, 
            "date_text": date_text
        })   
        
    # Calculate and format hours
    hours = list(range(0, 24))
    disabled_hours = [2, 3, 4, 5, 6]
    hours = list(filter(lambda hour: hour not in disabled_hours, hours))
    hours = list(map(lambda hour: f"0{hour}" if len(str(hour)) == 1 else str(hour), hours))  
    print (hours)  
    
    # Calculate free hours for streams
    available_hours = {}
    for day in available_days:
        if day["disabled"] == False:
            day_name = day["name"]
            day_num = day["num"]
            current_date = day["date"]
            day_streams = models.Stream.objects.filter(datetime__date=current_date).values('datetime').annotate(dcount=Count('datetime')).order_by("datetime")
            day_streams = day_streams.filter(dcount__gt=1)
            day_streams_hours = list(map(lambda stream: stream["datetime"].astimezone(user_time_zone).hour, day_streams))
            day_available_hours = list(map(lambda hour: str(hour), filter(lambda hour: hour not in day_streams_hours, hours)))
            day_available_hours = list(map(lambda hour: f"0{hour}" if len(str(hour)) == 1 else str(hour), day_available_hours))
            available_hours[day_name] = day_available_hours
        
    
    # Render page
    return render(request, 'app/schedule.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "error": error,
        "current_page": "schedule",
        
        # User profile context
        "profile_image": profile_image,
        "general_points_num": general_points_num,
        "weekly_points_num": weekly_points_num,
        "daily_points_num": daily_points_num,
        "ranking": user.ranking.name,
        "profile_card_layout": "horizontal",
        
        # Specific context
        "streams": streams,
        "available_days": available_days,
        "available_hours": available_hours,
        "time_zone": tools.get_time_zone_text(user),
        "hours": hours,
        "today_week_name": today_week_name,
    })

@decorators.validate_login_active
def support(request):
    """ Page for show live streamers and copy link to stream """
    
    user, message, _ = tools.get_cookies_data(request)
    profile_image = user.picture
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
    
    # Validate if node server its running
    is_node_working = twitch.is_node_working()

    # Valide if node server is working
    error = ""
    if not is_node_working:
        error = "El bot no está disponible en este momento (tus puntos no serán contabilizados)"

    # Get current streams and format
    current_streams = twitch.get_current_streams()
    if not current_streams:
        current_streams = []
    streams = [{"user": stream.user.user_name, "picture": stream.user.picture} for stream in current_streams]
    
    # Culate time of the user
    user_timezone = user.time_zone.time_zone
    user_time = datetime.datetime.now(pytz.timezone(user_timezone)).strftime("%I %p")
    
    # Calculate next stream
    next_stream_date_timezone = None
    if not streams:
        # Get date ranges
        logger.debug ("Getting hour of the next stream")
        now = timezone.now()
        start_datetime = datetime.datetime(
            now.year, now.month, now.day, now.hour, 0, 0, tzinfo=timezone.utc)
        end_datetime = start_datetime + datetime.timedelta(days=1)

        # Get next streams
        next_stream = models.Stream.objects.filter(
            datetime__range=[start_datetime, end_datetime]).order_by("datetime").first()
        
        # Get time of the next stream with timezone
        if next_stream:
            next_stream_date = next_stream.datetime
            next_stream_date_timezone = next_stream_date.astimezone (pytz.timezone(user_timezone)).strftime("%I %p")
    
    # Validate if the user is streaming right now
    user_streaming = False
    if list(filter (lambda stream: stream.user == user, current_streams)):
        user_streaming = True
    
    # Gerate referral link
    referral_link = f"{HOST}landing?referred={user.user_name}"

    # Render page
    return render(request, 'app/support.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "current_page": "support",
        "error": error,
        
        # User profile context
        "profile_image": profile_image,
        "general_points_num": general_points_num,
        "weekly_points_num": weekly_points_num,
        "daily_points_num": daily_points_num,
        "ranking": user.ranking.name,
        "profile_card_layout": "vertical",
        
        # Specific context
        "streams": streams,
        "next_stream_time": next_stream_date_timezone,
        "user_time": user_time,
        "user_timezone": tools.get_time_zone_text(user),
        "user_streaming": user_streaming,
        "referral_link": referral_link
    })

@decorators.validate_login_active
def ranking(request):
    """ Page for show the live ranking of the users based in points """
    
    # Get user data
    user, message, _ = tools.get_cookies_data(request)
    profile_image = user.picture
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points (user)
    
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
        "general_points_num": general_points_num,
        "weekly_points_num": weekly_points_num,
        "daily_points_num": daily_points_num,
        "ranking": user.ranking.name,
        "profile_card_layout": "horizontal small",
        
        # Specific context
        "ranking_today": ranking_today,
        "ranking_global_top": ranking_global_top,
        "ranking_global_other": ranking_global_other,
    })

@decorators.validate_login_active
def profile(request):
    """ Page for show and update the user data """
    
    user, message, _ = tools.get_cookies_data(request)

    # Render page
    return render(request, 'app/profile.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "profile"
    })

@decorators.validate_login_active
def wallet(request):
    """ Page for withdraw bits to wallet """
    
    user, message, _ = tools.get_cookies_data(request)

    # Render page
    return render(request, 'app/wallet.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "wallet"
    })
    
def testing (request):
    """ Page for tests """

    dari = models.User.objects.filter(user_name='darideveloper').first()
    
    live = twitch.is_user_live(dari)
    
    return HttpResponse(live)

@decorators.validate_login_active
@decorators.validate_admin
def user_points (request):
    """ Display points for all users, to admins only """
    
    # Get all users
    users_data = []
    users = models.User.objects.all()
    for user in users:
        
        *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points(user)
        
        users_data.append ({
            "link": f"{HOST}/admin/app/user/{user.id}/change/",
            "id": user.id,
            "user_name": user.user_name,
            "ranking": user.ranking.name,
            "email": user.email,
            "generals": general_points_num,
            "weekly": weekly_points_num,
            "daily": daily_points_num,
        })
    
    return render(request, 'app/users_points.html', {
        "current_page": "users-points",
        "users": users_data,
    })

@decorators.validate_login_active
def cancel_stream (request, id):
    
    # Get stream
    stream = models.Stream.objects.filter(id=id).first()
    
    # Get current user
    user, *other = tools.get_cookies_data(request)

    # Validate if stream is cancelable
    is_cancellable = tools.is_stream_cancelable(stream)

    # Validtae if the user is the owner of the stream, for delete it
    if stream.user == user:
        
        # Discount points to user
        if not is_cancellable:            
            tools.set_negative_point (user, 50, "penalización por cancelar stream")
        
        # Delete stream
        stream.delete()
        request.session["message"] = "Stream elminado."  
    else:  
        request.session["error"] = "Ha ocurrido un error al borrar el stream. Intente de nuevo mas tarde."
    
    # redirect
    return redirect('schedule')
    