import os
import pytz
import random
import datetime
from . import tools
from . import models
from . import decorators
from .twitch import TwitchApi
from django.conf import settings
from dotenv import load_dotenv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, Q
from django.template.loader import render_to_string
from botcheers import models as cheer_models

# Get credentials
load_dotenv()
HOST = os.environ.get("HOST")
SCHEDULE_DAY = int(os.environ.get("SCHEDULE_DAY"))
INFO = os.environ.get("INFO")
WITHDRAW_ENABLED = os.environ.get("WITHDRAW_ENABLED") == "True"

# Twitch instance
twitch = TwitchApi("Views App")

# Logs
log_origin_name = "Views App"
log_origin = models.LogOrigin.objects.get(name=log_origin_name)
log_type_error = models.LogType.objects.get(name="error")

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
        user_id, user_email, user_picture, user_name = twitch.get_user_info(
            user_token)

        # Validate user data
        if user_id and user_picture and user_name:

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
                new_user.ranking = lower_ranking

            # Save user id in session and tookens
            new_user.access_token = user_token
            new_user.refresh_token = refresh_token

            # Save data
            new_user.save()

            # Submit again stream to node if the user is streaming
            current_streams = twitch.get_current_streams()
            current_streams_users = list(
                map(lambda stream: stream.user.id, current_streams))
            if user_id in current_streams_users:
                twitch.submit_streams_node()

            request.session["user_id"] = new_user.id

        else:
            # Araise error when user data is not valid
            error = True
            if user_id:
                models.Log.objects.create(
                    origin=log_origin,
                    details=f" datos de usuario: {user_id}, {user_email}, {user_picture}, {user_name}",
                    log_type=log_type_error,
                )

    else:
        # Araise error where there it nor a login code
        error = True
        models.Log.objects.create(
            origin=log_origin,
            details="Error al obtener codigo de login",
            log_type=log_type_error,
        )

    if error:
        # Save login error in session
        request.session["error"] = "Error al iniciar sesión con twitch. Intente de nuevo mas tarde. Si el problema persiste, contacte a soporte."

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

    # Get user from cookies
    user_active = False
    user, *other = tools.get_cookies_data(request)
    cta_text = "Inicia sesión con twitch"
    if user:
        user_active = user.is_active
        cta_text = "Ir a apoyar"
        twitch_link = f"/support"

    # Render page with twitch link and error message (is exist)
    return render(request, 'app/landing.html', {
        "twitch_link":  twitch_link,
        "error": error,
        "current_page": "landing",
        "user_active": user_active,
        "cta_text": cta_text,
        "hide_menu": True,
    })


@decorators.validate_login
def whatsapp(request):
    """ Page for request whatsapp validation """

    # Get user from cookies
    user_active = False
    user_registed = True
    user, *other = tools.get_cookies_data(request)
    if user:
        user_active = user.is_active

        if not user.first_name or user.first_name.strip() == "":
            user_registed = False

    # redirect to home
    if user_active:
        return redirect("home")

    # redirect to register
    if not user_registed:
        return redirect("register")

    return render(request, 'app/whatsapp.html', {
        "current_page": "whatsapp",
        "user_active": False,
        "hide_menu": True,
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


@decorators.validate_login
def register(request):
    """ Page for complete register, after login with twitcyh the first time """

    # timezones = pytz.all_timezones

    # Get user from cookies
    user, message, error = tools.get_cookies_data(request)

    # Redirect to home if user id is not valid
    if not user or (user.first_name and user.first_name.strip() != ""):
        return redirect("home")

    if request.method == "POST":

        # Get user data from form
        first_name = request.POST.get("first-name", "")
        last_name = request.POST.get("last-name", "")
        country_name = request.POST.get("country", "")
        time_zone_name = request.POST.get("time-zone", "")
        phone = request.POST.get("full-phone", "")

        if first_name and last_name and country_name and time_zone_name and phone:

            # Create country and time zone objects
            country = tools.get_create_country(country_name)
            time_zone = tools.get_create_time_zone(time_zone_name)

            # Update user data
            user.first_name = first_name
            user.last_name = last_name
            user.country = country
            user.time_zone = time_zone
            user.phone = tools.clean_phone(phone)

            # Update referred user from
            user_from_id = request.session.get("user_from_id", "")
            if user_from_id:
                user_froms = models.User.objects.filter(id=user_from_id)
                if user_froms:
                    user_from = user_froms.first()
                    user.referred_user_from = user_from

            # Save
            user.save()

            # Save message for show in home page
            request.session["message"] = "Registro completado con éxito"

            # Redirect to home
            return redirect("home")

        else:
            # Show error if data is not valid
            request.session["error"] = "Algo salió mal, intente de nuevo"

    # Default response
    return render(request, 'app/register.html', {
        "id": user.id,
        "email": user.email,
        "picture": user.picture,
        "user_name": user.user_name,
        "current_page": "register",
        "user_active": False,
        "country": "México",
        "time_zone": "America/Mexico_City",
        "error": error,
        "hide_menu": True,
    })


def error404(request, exception):
    # Render template 404.html
    rendered = render_to_string('app/404.html', {
        # General context
        "name": "",
        "current_page": "404",
        "user_active": False,
    })
    return HttpResponse(rendered)


def logout(request):
    """ Logout user """

    # Delete user id from cookies
    if "user_id" in request.session:
        del request.session["user_id"]
        # request.session["required_logout"] = False

    # Redirect to home
    return redirect("home")


@decorators.validate_login_active
def points(request):
    """ Page for show the points of the user """

    # Get user data
    user, message, _ = tools.get_cookies_data(request)
    profile_image = user.picture
    general_points, weekly_points, daily_points, \
        general_points_num, weekly_points_num, daily_points_num = tools.get_user_points(
            user)

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
        datetime_user = point.datetime.astimezone(
            pytz.timezone(user_time_zone))
        date = datetime_user.strftime("%d/%m/%Y")
        time = datetime_user.strftime("%I %p")
        channel = ""

        # Detail info of negative points
        details = point.details
        if not details and point.amount < 0:

            # Fix details for "viwer asistió a stream"
            if point.info.info == "viwer asistió a stream":
                details = f"Puntos restados por asistencia de {abs(point.amount)} viwers en tu stream"
            else:
                details = point.info

        # Point title
        title = point.info.info
        if title in ["faltó tiempo de visualización", "faltaron comentarios"]:
            title = "Punto no obtenido"
        elif title in ["reclamación de puntos sin evidencia", "penalización por cancelar stream", "penalización por no abrir stream a tiempo"]:
            title = "Penalización"
        elif title in ["viwer asistió a stream"]:
            title = "Asistencia de viwers a stream"

        # stream name
        if point.stream and point.info:
            channel = f"{point.stream.user.user_name}"

        points_data.append({
            "date": date,
            "time": time,
            "my_points": current_points,
            "points": point.amount,
            "chanel": channel,
            "details": details,
            "user_active": True,
            "title": title,
        })

        # Decress punits counter
        current_points -= point.amount

    # Render page
    return render(request, 'app/points.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "current_page": "points",
        "user_active": True,
        "hide_menu": False,

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
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points(user)
    user_time_zone = pytz.timezone(user.time_zone.time_zone)
    print(user_time_zone)

    # Get if the user has vips and frees
    has_vips = tools.get_vips_num(user) > 0
    has_frees = tools.get_frees_num(user) > 0

    # Get today week day
    now = timezone.now().astimezone(user_time_zone)
    today_week = now.weekday()
    today_week_name = tools.WEEK_DAYS[today_week]

    # Validate if stream can be saved, in post
    if request.method == "POST":

        # Get next streams of the user in the next 7 days
        streams = tools.get_user_streams(user, user_time_zone)
        user_streams_num = len(streams)

        # Get stream data
        form_date = request.POST.get("date", "")
        form_hour = request.POST.get("hour", "")
        form_vip = request.POST.get("vip", "")
        form_free = request.POST.get("free", "")

        # Convert to datetime
        selected_datetime = datetime.datetime.strptime(
            form_date + " " + form_hour+":00", "%Y-%m-%d %H:%M")
        selected_datetime = user_time_zone.localize(selected_datetime)

        min_points_save_stream = int(models.Settings.objects.get(
            name="min_points_save_stream").value)

        # Calculate available points
        available_points = general_points_num - \
            user_streams_num * min_points_save_stream

        # Validte if regular user have available streams
        max_streams = user.ranking.max_streams
        streams_extra = models.StreamExtra.objects.filter(user=user).all()
        if streams_extra.count() > 0:
            streams_extra_num = streams_extra.aggregate(Sum('amount'))[
                'amount__sum']
            max_streams += streams_extra_num

        available_stream = max_streams - user_streams_num > 0
        if not available_stream or available_points < min_points_save_stream:
            # Save error ass cookie
            request.session["error"] = f"Lo sentimos. No cuentas con ranking o puntos suficientes para agendar mas streams."
            return redirect("/schedule")

        # Validate if the date and time are free
        streams_match = models.Stream.objects.filter(
            datetime=selected_datetime)
        if streams_match.count() > 1:
            request.session["error"] = "Lo sentimos. Esa fecha y hora ya está agendada."
            return redirect("/schedule")

        # Validate if the date time is before now
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        selected_hour = selected_datetime.replace(
            minute=0, second=0, microsecond=0)
        if selected_datetime == current_hour:
            request.session["error"] = "Lo sentimos. Ya inició la hora, no puedes agendar."
            return redirect("/schedule")

        # Vips validation
        if form_vip:

            if has_vips:
                # Decrease vips
                negative_vip = models.StreamVip(user=user, amount=-1)
                negative_vip.save()

                # Get if the user has vips (again)
                has_vips = tools.get_vips_num(user) > 0
            else:
                request.session["error"] = "Lo sentimos. Ya no cuentas con streams VIP"
                return redirect("/schedule")

        # Frees validation
        if form_free:

            if has_frees:
                # Decrease frees
                negative_free = models.StreamFree(user=user, amount=-1)
                negative_free.save()

                # Get if the user has vips (again)
                has_frees = tools.get_frees_num(user) > 0
            else:
                request.session["error"] = "Lo sentimos. Ya no cuentas con streams VIP"
                return redirect("/schedule")

        # Schedule stream
        is_vip = True if form_vip else False
        is_free = True if form_free else False
        new_stream = models.Stream(
            user=user, datetime=selected_datetime, is_vip=is_vip, is_free=is_free)
        new_stream.save()
        request.session["message"] = "Stream agendado!"

        return redirect("/schedule")

    # Get next streams of the user in the next 7 days
    streams = tools.get_user_next_streams(user, user_time_zone)

    # Format streams date times
    streams_date_times = list(
        map(lambda stream: {"date": stream["date"], "hour": stream["hour"]}, streams))

    # Validate the open hour of the current user
    ranking_open = True
    open_hour = user.ranking.open_hour
    open_hour_datetime = datetime.datetime.combine(
        now.date(), open_hour).astimezone(user_time_zone)
    if today_week == SCHEDULE_DAY:
        ranking_open = False
        if now >= open_hour_datetime:
            ranking_open = True

    # Validate if today isn't sunday
    available_days = []
    available_hours = {"domingo": []}
    hours = []
    visible_schedule_panel = True
    if ranking_open:

        # Get available days of the week
        for day_num in range(0, 6):

            extra_days = 0
            if today_week == SCHEDULE_DAY:
                extra_days = 7

            # Calculate dates
            day_name = tools.WEEK_DAYS[day_num]
            date = now + datetime.timedelta(days=day_num-today_week+extra_days)
            date_text_day = date.strftime("%d")
            date_text_month = date.strftime("%B")
            date_text_month_spanish = tools.MONTHS[date_text_month]
            date_text = f"{date_text_day} de {date_text_month_spanish}"
            date_formatted = date.strftime("%Y-%m-%d")

            # Date status
            disabled = False
            active = False
            if today_week != SCHEDULE_DAY:
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
        disabled_hours = [0, 1, 2, 3, 4, 5, 6]

        # Convert disable hours to user time zon
        system_time_zone = pytz.timezone(settings.TIME_ZONE)
        disabled_hours_timezone = list(map(lambda hour: system_time_zone.localize(
            datetime.datetime(
                now.year,
                now.month,
                now.day,
                int(hour),
                now.minute,
                now.second,
                0
            )), disabled_hours
        ))
        disabled_hours = list(map(lambda hour: hour.astimezone(
            user_time_zone).hour, disabled_hours_timezone))

        # Disable hour by days
        disabled_hours_days = {
            "lunes": 22,
            "martes": 22,
            "miercoles": 22,
            "jueves": 22,
        }

        # Calculate free hours for streams
        for day in available_days:
            if day["disabled"] == False:

                # Generate hours
                hours = list(range(0, 24))
                if day["num"] == today_week:
                    hours = list(
                        filter(lambda hour: hour > int(now.hour), hours))
                hours = list(
                    filter(lambda hour: hour not in disabled_hours, hours))
                hours = list(map(lambda hour: f"0{hour}" if len(
                    str(hour)) == 1 else str(hour), hours))

                # Day variables
                day_name = day["name"]
                day_num = day["num"]
                current_date = day["date"]

                # get streams of the day
                day_streams = models.Stream.objects.filter(datetime__date=current_date).values(
                    'datetime').annotate(dcount=Count('datetime')).order_by("datetime")
                day_streams = day_streams.filter(
                    Q(dcount__gt=1) | Q(is_vip=True))

                # Calculate free hours
                day_streams_hours = list(map(lambda stream: stream["datetime"].astimezone(
                    user_time_zone).strftime("%H"), day_streams))
                day_available_hours = list(map(lambda hour: str(hour), filter(
                    lambda hour: hour not in day_streams_hours, hours)))
                day_available_hours = list(map(lambda hour: f"0{hour}" if len(
                    str(hour)) == 1 else str(hour), day_available_hours))
                available_hours[day_name] = day_available_hours

        # Remove disable hour by days
        for day_name, hour in disabled_hours_days.items():

            hour_timezone = datetime.datetime(
                now.year, now.month, now.day, hour, now.minute, now.second, 0).astimezone(user_time_zone).strftime("%H")

            if day_name in available_hours:
                available_hours[day_name] = list(
                    filter(lambda hour: hour != hour_timezone, available_hours[day_name]))

    else:
        visible_schedule_panel = False

    # Get ranking data without admin
    ranking_data = models.Ranking.objects.all().order_by("-id")
    ranking_data = list(filter(lambda ranking:
                               ranking.name not in ["admin", "platino"],
                               ranking_data))

    # Cobvert ranking times to user timezone
    randing_data_formated = []
    for ranking in ranking_data:

        open_hour = ranking.open_hour
        ranking_name = ranking.name
        max_streams = ranking.max_streams

        # Convert open hour (time) to datetime
        open_hour_datetime = datetime.datetime.combine(
            now.date(), open_hour).astimezone(user_time_zone)
        
        # Save hour as string in format 00:00
        open_hour = open_hour_datetime.strftime("%H:%M")
        
        # Return data to ranking
        randing_data_formated.append ({
            "open_hour": open_hour,
            "name": ranking_name,
            "max_streams": max_streams,
        })
        

    # Render page
    return render(request, 'app/schedule.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "error": error,
        "current_page": "schedule",
        "user_active": True,
        "hide_menu": False,

        # User profile context
        "profile_image": profile_image,
        "general_points_num": general_points_num,
        "weekly_points_num": weekly_points_num,
        "daily_points_num": daily_points_num,
        "ranking": user.ranking.name,
        "profile_card_layout": "horizontal",

        # Specific context
        "streams": streams,
        "streams_date_times": streams_date_times,
        "available_days": available_days,
        "available_hours": available_hours,
        "time_zone": tools.get_time_zone_text(user),
        "hours": hours,
        "today_week_name": today_week_name,
        "has_vips": has_vips,
        "has_frees": has_frees,
        "visible_schedule_panel": visible_schedule_panel,
        "rankings_data": randing_data_formated,
    })


@decorators.validate_login_active
def support(request):
    """ Page for show live streamers and copy link to stream """

    user, message, error = tools.get_cookies_data(request)
    profile_image = user.picture
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points(user)

    # Validate if the current user its admin and donnot
    is_admin = tools.get_admin_type(user)
    is_donnor = user.is_donnor
    is_admin_donnor = is_admin and is_donnor

    # Save new donation status from post
    if is_admin_donnor and request.method == "POST":

        # get variables from form
        stream_id = request.POST.get("stream")
        donation = request.POST.get("donation")

        # Get stream
        streams_donation = models.Stream.objects.filter(id=stream_id)
        if not streams_donation:
            request.session["error"] = "Error al guardar la donación"
        stream_donation = streams_donation[0]

        # get bit object
        bits = models.Bit.objects.filter(stream=stream_donation)
        if not bits:
            request.session["error"] = "Error al guardar la donación"
        bits = bits[0]

        # Update status
        bits.is_bits_done = True if donation == "on" else False
        bits.save()

        return redirect("support")

    # Get current streams and format
    streams = []
    current_streams = twitch.get_current_streams()
    if not current_streams:
        current_streams = []
    for stream in current_streams:
        stream_user = tools.get_fix_user(stream.user)
        bits_claimed = models.Bit.objects.filter(stream=stream)
        claimed_bits = bits_claimed.aggregate(Sum('amount'))["amount__sum"]
        if claimed_bits:
            claimed_bits = abs(claimed_bits)
        else:
            claimed_bits = 0

        is_bits_done = False
        if bits_claimed:
            is_bits_done = bits_claimed[0].is_bits_done if bits_claimed else False

        streams.append({
            "id": stream.id,
            "user": stream_user.user_name,
            "picture": stream_user.picture,
            "is_vip": stream.is_vip,
            "claimed_bits": claimed_bits,
            "is_bits_done": is_bits_done,
        })

    # Culate time of the user
    user_timezone = user.time_zone.time_zone
    user_time = datetime.datetime.now(
        pytz.timezone(user_timezone)).strftime("%I %p")

    # Calculate next stream
    next_stream_date_timezone = None
    if not streams:
        # Get date ranges
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
            next_stream_date_timezone = next_stream_date.astimezone(
                pytz.timezone(user_timezone)).strftime("%I %p")

    # Validate if the user is streaming right now
    user_streaming = False
    if list(filter(lambda stream: stream.user == user, current_streams)):
        user_streaming = True

    # Gerate referral link
    referral_link = tools.get_referral_link(user)

    # Default info from environment variables
    info = INFO

    # Validate if is triple time and show message
    is_triple_time = tools.is_triple_time()
    if is_triple_time and not message:
        info = "Felicidades! Recibirás 3 veces los puntos por cada stream que veas en esta hora"

    # info = "¡Importante! Ya se están corregiendo los puntos diarios negativos y los puntos generales faltantes. No es necesario hacer un ticket de soporte."

    # Render page
    return render(request, 'app/support.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "info": info,
        "current_page": "support",
        "error": error,
        "user_active": True,
        "hide_menu": False,

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
        "referral_link": referral_link,
        "is_admin_donnor": is_admin_donnor,
    })


@decorators.validate_login_active
def ranking(request):
    """ Page for show the live ranking of the users based in points """

    # Get user data
    user, message, _ = tools.get_cookies_data(request)
    profile_image = user.picture
    *other, general_points_num, weekly_points_num, daily_points_num = tools.get_user_points(user)

    # Get the top 10 users from TopDailyPoint, ordered by amout and date
    top_daily_points = models.TopDailyPoint.objects.all().order_by("-amount", "datetime")

    position = 1
    ranking_today = []
    for rank in top_daily_points:
        ranking_today.append({
            "position": position,
            "user": rank.user.user_name,
            "amount": rank.amount,
        })
        position += 1

    # Get top 10 users from general points
    points_history = models.PointsHistory.objects.all().order_by(
        "general_points_week_num", "general_points_num").reverse()[:10]
    ranking_global = [[index + 1, register.user.user_name, register.general_points_week_num, f'app/imgs/icon_{register.user.ranking}.png', register.user.picture, register.user.ranking]
                      for index, register in enumerate(points_history)]
    ranking_global_top = ranking_global[:3]
    ranking_global_other = ranking_global[3:]

    # Render page
    return render(request, 'app/ranking.html', {
        # General context
        "name": user.user_name,
        "message": message,
        "user_active": True,
        "hide_menu": False,

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

    user, message, error = tools.get_cookies_data(request)

    # Update user data in post
    if request.method == "POST":

        # Get country and time zone from form
        country_name = request.POST.get("country")
        time_zone_name = request.POST.get("time-zone")
        phone = request.POST.get("phone")

        # Clean phgone number
        phone = tools.clean_phone(phone)

        # Create country and time zone objects
        country = tools.get_create_country(country_name)
        time_zone = tools.get_create_time_zone(time_zone_name)

        # Update user data
        user.country = country
        user.time_zone = time_zone
        user.phone = phone
        user.save()

        # Confirmation message
        message = "Datos actualziados correctamente"

        return redirect("/profile")

    # Get user data
    twitch_id = user.id
    email = user.email
    user_name = user.user_name

    twitch_refresh_link = "/update-twitch-data/"
    country = user.country
    time_zone = user.time_zone
    phone = user.phone

    # Get referrals
    referred_users = models.User.objects.filter(referred_user_from=user)
    referrals = list(
        map(lambda user: {"user": user.user_name, "points": 100}, referred_users))

    # Get referral link
    referral_link = tools.get_referral_link(user)

    # Render page
    return render(request, 'app/profile.html', {
        "name": user.user_name,
        "message": message,
        "error": error,
        "current_page": "profile",
        "user_active": True,
        "hide_menu": False,

        # User profile context
        "current_page": "profile",
        "profile_image": user.picture,
        "ranking": user.ranking.name,

        # Specific context
        "twitch_id": twitch_id,
        "phone": phone,
        "twitch_refresh_link": twitch_refresh_link,
        "country": country,
        "time_zone": time_zone,
        "referrals": referrals,
        "referral_link": referral_link,
        "user_name": user_name,
        "email": email,
    })


@decorators.validate_login_active
def wallet(request):
    """ Page for withdraw bits to wallet """

    user, message, _ = tools.get_cookies_data(request)

    # Get bits of the current user
    bits, bits_num = tools.get_bits(user)

    if request.method == "POST" and bits_num > 0:

        # Add bits to stream
        stream_id = request.POST.get("stream")
        stream = models.Stream.objects.get(id=stream_id)
        stream.save()

        # Add register for claim bits
        bits_app = models.Bit(user=user, amount=-bits_num,
                              details="Bits reclamados", stream=stream)
        bits_app.save()

        # Get donations bot
        donatins_bot = cheer_models.User.objects.filter(name="Comunidad_MC")
        if donatins_bot and donatins_bot[0].is_active:

            # register donation
            donation_datetime = stream.datetime.astimezone(
                pytz.timezone("America/Mexico_City"))
            rand_min = random.randint(10, 40)
            donation_datetime = donation_datetime.replace(minute=rand_min)
            cheer_models.Donation.objects.create(
                user=donatins_bot[0],
                stream_chat_link=f"https://www.twitch.tv/popout/{user.user_name}/chat?popout=",
                datetime=donation_datetime,
                amount=bits_num,
                message=random.choice([
                    "",
                    "Buen stream",
                    "Eres el mejor",
                    "Gracias por el stream",
                    "Sigue así",
                    "Sorry por la demora",
                    "Aquí están los bits",
                    "Un pequeño aporte",
                    "No es mucho, pero es lo que tengo, suerte crack",
                    "Me encanta tu contenido",
                    "Me encantan tus streams",
                ]),
                bits_app=bits_app,
            )
        else:
            models.Log.objects.create(
                origin=log_origin,
                details="Auto donations bot not found or inactive",
                log_type=log_type_error,
            )

        # Update bits of the user
        bits, bits_num = tools.get_bits(user)

        return redirect("/wallet")

    # Format bits history
    bits_history = list(map(lambda bit: {"date": bit.timestamp.strftime(
        "%d/%m/%Y"), "bits": bit.amount, "description": bit.details}, bits))

    # Get streams of the current user
    user_time_zone = pytz.timezone(user.time_zone.time_zone)
    streams = tools.get_user_next_streams(user, user_time_zone)
    # streams = list(map(lambda stream: {"id": stream["id"], "datetime": stream["datetime"]}, user_streams_data))

    # Select bits icon
    bits_amount_range = {
        "d": 5000,
        "c": 1000,
        "b": 100,
        "a": 0,
    }
    for bit_name, bit_min in bits_amount_range.items():
        if bits_num >= bit_min:
            bits_icon = f"app/imgs/icon_bits_{bit_name}.gif"
            break

    # Render page
    return render(request, 'app/wallet.html', {
        "name": user.user_name,
        "message": message,
        "current_page": "wallet",
        "user_active": True,
        "hide_menu": False,

        # User profile context
        "profile_image": user.picture,
        "ranking": user.ranking.name,

        # Specific context
        "bits": bits_num,
        "streams": streams,
        "history": bits_history,
        "bits_icon": bits_icon,
        "withdraw_enabled": WITHDRAW_ENABLED,
    })


def testing(request):
    """ Page for tests """

    return HttpResponse("ok")


@decorators.validate_login_active
@decorators.validate_admin
def calendar(request):
    """ Page for show the calendar of the streams """

    streams = models.Stream.objects.all().order_by("datetime")

    # Filter only next streams, and streams of the last 7 days
    start_date = timezone.now() - datetime.timedelta(days=2)
    streams = list(
        filter(lambda stream: stream.datetime > start_date, streams))

    # Format streams data
    streams_data = []
    for stream in streams:

        # Locate date in time zone
        date = stream.datetime.astimezone(pytz.timezone("America/Mexico_City"))

        # Check claim bits in stream
        bits_num = 0
        bits_claimed = models.Bit.objects.filter(stream=stream, amount__lt=0)
        bits_done = False
        if bits_claimed:
            bits_claimed = bits_claimed.first()
            bits_num = abs(bits_claimed.amount)
            if bits_claimed.is_bits_done:
                bits_done = True

        # Generate url of admin (stream url or bits url)
        if bits_claimed:
            url = f"/admin/app/bit/{bits_claimed.id}/change/"
        else:
            url = f"/admin/app/stream/{stream.id}/change/"

        # Format and save
        streams_data.append({
            "user": stream.user.user_name,
            "start": date.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": (date + datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "bits": bits_num,
            "bits_done": str(bits_done),
            "url": url,
        })

    # Render page
    return render(request, 'app/calendar.html', {
        # General context
        "current_page": "calendar",
        "user_active": True,
        "hide_menu": False,

        # Specific context
        "streams": streams_data,
    })


@decorators.validate_login_active
def cancel_stream(request, id):

    error = "Ha ocurrido un error al borrar el stream. Intente de nuevo mas tarde."

    # Get stream
    stream = models.Stream.objects.filter(id=id).first()

    # Validate if stream exists
    if not stream:
        request.session["error"] = error
        return redirect('schedule')

    # Get current user
    user, *other = tools.get_cookies_data(request)

    # Validate if stream is cancelable
    is_cancellable = tools.is_stream_cancelable(stream)

    # Validtae if the user is the owner of the stream, for delete it
    if stream.user == user:

        if is_cancellable:
            # Remove negative vip
            negative_vip = models.StreamVip.objects.filter(
                user=user, amount=-1).first()
            if negative_vip:
                negative_vip.delete()

            # Remove negative free
            negative_free = models.StreamFree.objects.filter(
                user=user, amount=-1).first()
            if negative_free:
                negative_free.delete()

        else:
            # Discount points to user
            tools.set_negative_point(
                user, 50, "penalización por cancelar stream", None, log_origin_name)

            # # Add a negative extra stream
            # models.StreamExtra(user=user, amount=-1).save()

        # Delete stream
        stream.delete()

        request.session["message"] = "Stream elminado."
    else:
        request.session["error"] = error

    # redirect
    return redirect('schedule')


@csrf_exempt
def update_twitch_data(request):
    """ Update user data from twitch """

    # Get user data
    user, *other = tools.get_cookies_data(request)

    updated = twitch.update_twitch_data(user)

    # Redirect
    if updated:
        request.session["message"] = "Datos actualizados desde Twitch."
    else:
        request.session["error"] = "Error al actualizar. Intenta cerrar sesión. Si sigues viendo este mensaje, contacta al administrador."
    return redirect('profile')


def register_referred_user_from(request, user_from_id):
    """ Save cookie from user that referred, and reciredt to home """

    # Get referred user from
    referred_users = models.User.objects.filter(id=user_from_id)
    if referred_users:
        referred_user = referred_users.first()

        # Save cookie with id
        request.session["user_from_id"] = referred_user.id

        # Redirect to landing
        return redirect('landing')
