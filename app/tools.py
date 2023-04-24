import os
import pytz
from . import models
from . import tools
import requests as req
from .logs import logger
from django.conf import settings 
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta

# Get enviroment variables
HOST = os.environ.get("HOST")
TRIPLE_POINTS_END = os.environ.get("TRIPLE_POINTS_END")
TRIPLE_POINTS_START = os.environ.get("TRIPLE_POINTS_START")

# Shared const
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

def get_fix_user (user:models.User):
    """ get user and fix profile image if not exist

    Args:
        user (models.User): User object

    Returns:
        user: user object with fixed profile image
    """
        
    user_picture = user.picture
    online_picture = True
        
    if not "/static/" in user_picture:
        
        # Try to get image from url
        try:
            res = req.get (user_picture)
        except:
            online_picture = False
        else:        
            if not res.status_code == 200:
                online_picture = False
        
        # Check picture extension 
        valid_extension = False
        valid_extensions = [".jpg", ".png", ".jpeg", ".gif"]
        for ext in valid_extensions:
            if ext in user_picture:
                valid_extension = True
                break
                        
        # Use profile image if error
        if not valid_extension or not online_picture:
            user.picture = "/static/app/imgs/profile.png"
            # user.save()
            
    # Return user with new profile image
    return user

def get_cookies_data (request, delete_data:bool=True):
    """ Get user and message from cookies

    Returns:
        touple: user object, menssaje text, error text
    """

    # Force to close sessión 1 time
    cookies_deleted = request.session.get("cookies_deleted", False)
    if not cookies_deleted:
        
        # Delete user from cookies
        request.session["user_id"] = 0
        request.session["cookies_deleted"] = True
    
    # Get user data from cookies
    user_id = request.session.get("user_id", 0)
    # user_id = 226645357
    users = models.User.objects.filter(id=user_id)
    
    # Delete cookies if user not exist and return None
    if users.count() == 0:
        try:
            del request.session["user_id"]
        except:
            pass
        return None, "", ""
    
    # Get user and use default profile image if not exist
    user = get_fix_user(users.first())
    
    # Get message from cookies
    message = request.session.get("message", "")
    if message and delete_data:
        del request.session["message"]
        
    # Get error from cookies
    error = request.session.get("error", "")
    if error and delete_data:
        del request.session["error"]
    
    return user, message, error

def get_vips_num (user:models.User):
    """ return the number of vip (only counter) streams of the user

    Args:
        user (models.User): user object

    Returns:
        int: counter of vips
    """
    
    vips_num = 0
    vips = models.StreamVip.objects.filter(user=user)
    if vips:
        vips_num = vips.aggregate(Sum('amount'))['amount__sum']
    
    return vips_num
    
    
def get_general_points (user:models.User):
    """ Return the general points (registers and counters) from specific user

    Args:
        user (:models.User): user object

    Returns:
        touple: general_points (registers), general_points_num (counter)
    """
    
    general_points = models.GeneralPoint.objects.filter(user=user).order_by("datetime").reverse()
        
    # Filter general points of the date before current hour
    now_datetime = timezone.now().astimezone(pytz.timezone (settings.TIME_ZONE)) 
    last_hour = now_datetime.replace(minute=0, second=0, microsecond=0)
    # now_hour = int (now_datetime.strftime("%H"))
    general_points = general_points.filter(datetime__lt=last_hour)
    general_points_num = general_points.aggregate(Sum('amount'))['amount__sum']
    
    if not general_points_num:
        general_points_num = 0
    
    return general_points, general_points_num

def get_general_points_last_week (user:models.User):
    """ Return the general points (registers and counters) from specific user

    Args:
        user (:models.User): user object

    Returns:
        touple: general_points (registers), general_points_num (counter)
    """
    
    # Calculate general points of the current week
    general_points_week = models.GeneralPoint.objects.filter(user=user, datetime__week=timezone.now().isocalendar()[1])
    general_points_week_num = general_points_week.aggregate(Sum('amount'))['amount__sum']
    
    if not general_points_week_num:
        general_points_week_num = 0

    return general_points_week, general_points_week_num
    
def get_user_points (user:models.User):
    """ Get user point, count and register reguister and counters

    Args:
        user (models.User): user object

    Returns:
        touple: general_points, weekly_points, daily_points, general_points_num, weekly_points_num, daily_points_num
    """
    
    # get general points
    general_points, general_points_num = get_general_points(user)
    
    # get points registers
    weekly_points = models.WeeklyPoint.objects.filter(general_point__in=general_points)
    daily_points = models.DailyPoint.objects.filter(general_point__in=general_points)
    
    # Calculate sums of points
    weekly_points_num = weekly_points.aggregate(Sum('general_point__amount'))['general_point__amount__sum']
    daily_points_num = daily_points.aggregate(Sum('general_point__amount'))['general_point__amount__sum']
        
    if not weekly_points_num:
        weekly_points_num = 0
        
    if not daily_points_num:
        daily_points_num = 0
    
    return general_points, weekly_points, daily_points, general_points_num, weekly_points_num, daily_points_num

def get_time_zone_text (user): 
    """ Return user time zone as clen text

    Args:
        user (models.User): user object to get time zone from

    Returns:
        str: time zone as text
    """
    
    time_zone = str(user.time_zone.time_zone)
    return time_zone.replace("-", " ").replace("/", " / ").replace("_", " ")

def get_streams_formatted (streams:models.Stream, user_time_zone:pytz.timezone) -> dict:
    """ Format streams data to dictionary and return it

    Args:
        streams (models.Stream): streams intances
        user_time_zone (pytz.timezone): user time zone

    Returns:
        dict: dictionary of streams with: id, date, time, datetime, is_cancellable, hour, is_vip and date_formatted
    """
    
     # Format streams
    streams_data = []
    for stream in streams:
        id = stream.id
        stream_datetime = stream.datetime.astimezone(user_time_zone)
        date = stream_datetime.strftime("%Y-%m-%d")
        time = stream_datetime.strftime("%I:%M %p")
        time_24 = stream_datetime.strftime("%H:%M")
        datetime = stream_datetime.strftime("%Y-%m-%d %I:%M %p")
        hour = stream_datetime.strftime("%H")
        is_cancellable = is_stream_cancelable(stream)
        is_vip = stream.is_vip
        
        # Format date like: Lun, 01, Enero
        date_weekday_num = stream_datetime.weekday()
        date_month = stream_datetime.strftime("%B")
        date_day = stream_datetime.strftime("%d")
        date_formatted = f"{WEEK_DAYS[date_weekday_num].title()} {date_day}, {MONTHS[date_month]}"
        
        streams_data.append ({
            "id": id,
            "date": date, 
            "time": time, 
            "datetime": datetime,
            "is_cancellable": "regular" if is_cancellable else "warning",
            "hour": hour,
            "is_vip": is_vip,
            "date_formatted": date_formatted,
            "time_24": time_24,
        })
        
    return streams_data

     
def get_user_streams (user:models.User, user_time_zone:pytz.timezone):
    """ Return user streams for the next 7 days, and its proccessed data

    Args:
        user (models.User): user instance
        user_time_zone (pytz.timezone): time zone of the current user

    Returns:
        touple: user_streams (model Objects), user_streams_data (array)
    """
    
    logger.debug (f"Getting next streams of the user {user}")
    start_week = timezone.datetime.today()
    if start_week.weekday() != 6:
        start_week = start_week - timedelta(start_week.weekday())
    end_week = start_week + timedelta(14)
        
    # Get current streams
    user_streams = models.Stream.objects.filter(
        datetime__range=[start_week, end_week], user=user).all().order_by("datetime")
    
    if not user_streams:
        user_streams = []
        
    # Format and return streams
    streams_formatted = get_streams_formatted(user_streams, user_time_zone)
    return streams_formatted
        
   
def get_user_next_streams (user:models.User, user_time_zone:pytz.timezone):
    """ Return the next streams of the user

    Args:
        user (models.User): user instance
        user_time_zone (pytz.timezone): time zone of the current user

    Returns:
        touple: user_streams (model Objects), user_streams_data (array)
    """
    
    # Get all stream of the current week
    # streams = get_user_streams(user, user_time_zone)
    
    # Filter only njext streams
    now = timezone.now().astimezone(user_time_zone)
    user_streams = models.Stream.objects.filter(
        datetime__gt=now, 
        user=user
    ).all().order_by("datetime")
    
    # Format and return streams
    streams_formatted = get_streams_formatted(user_streams, user_time_zone)
    return streams_formatted

def is_stream_cancelable (stream):
    """ Return if stream is cancelable or not

    Args:
        stream (models.Stream): stream object

    Returns:
        bool: True if stream is cancelable, False if not
    """
    
    if stream:
        return stream.datetime > ( timezone.now() + timedelta(hours=1) )
    else:
        return False

def set_negative_point (user:models.User, amount:int, reason:str, stream:models.Stream):
    """ Set negative point to user if it is possible

    Args:
        user (models.User): user to set points
        amount (int): number of negative points to set
        reason (str): info_point text
        
    Returns:
        bool: True if point was set, False if not
    """
    
    amount = abs(amount)
    
    # Validate if user has enough points
    _, general_points_num_streamer = tools.get_general_points (user)
    if not general_points_num_streamer or general_points_num_streamer < amount:
        amount = general_points_num_streamer
                
    if amount <= 0:
        return False
        
    logger.info (f"Adding {amount} negative points to {user} for: {reason}")
    
    # Get info point
    info_point = models.InfoPoint.objects.get (info=reason)
    if not info_point:
        info_point = models.InfoPoint (info=reason)
        info_point.save ()
    
    # Search if already exist nevative a point for the stream
    general_points = models.GeneralPoint.objects.filter (user=user, info=info_point)
    if general_points:
        
        # Incress negative point
        general_point = general_points.first()
        general_point.amount -= amount
        general_point.save()
        
    else:
                
        # Add new point
        general_point = models.GeneralPoint (user=user, datetime=timezone.now(), amount=-amount, info=info_point)
        general_point.save ()
    
    return True
    
def is_triple_time ():
    """ Check if the current time (with time zone of the project) is triple time

    Returns:
        bool: True if triple time, False if not
    """
    
    # Get current time
    now_str = timezone.localtime().strftime ("%H:%M")
    now_time = datetime.strptime(now_str, "%H:%M")
    
    # Convert triple points times
    triple_time_start = datetime.strptime(TRIPLE_POINTS_START, "%H:%M")
    triple_end_time = datetime.strptime(TRIPLE_POINTS_END, "%H:%M")
    
    # add extra day to end time if its less than start time
    if triple_end_time < triple_time_start:
        triple_end_time = triple_end_time + timedelta(days=1)
        
    # Validate if the current time its in triple time
    return triple_time_start <= now_time <= triple_end_time

def get_admin_type (user:models.User = None, user_auth:models.UserAuth = None):
    """ Return admin type of the user, or user_auth

    Args:
        user (models.User): user model
        user_auth (models.UserAuth): user auth model

    Returns:
        str: name of the admin type if its admin, None if not
    """
    
    # Validate if there is the user or the user_auth
    if not user and not user_auth:
        return None
    
    # Get user auth
    if not user_auth:
        user_auth = user.user_auth 
        
    # Get user groups
    if user_auth:
        user_group = user_auth.groups.first ()
        
        # Validate if user has groups
        if user_group:
            user_group_name = user_group.name
            
            # Validate if user is admin
            if "admin" in user_group_name:
                return user_group_name
            
    # Default return
    return None

def get_referral_link (user:models.User):
    """ Generate referral link for the user

    Args:
        user (models.User): _description_
    """
    
    referral_link = f"{HOST}/register/{user.id}"
    return referral_link

def get_create_country (country_name:str):
    """ Return or create (if not exists) a country

    Args:
        country_name (str): country name
        
    Returns:
        models.Country: country instance
    """
    
    countries = models.Country.objects.filter(country=country_name)
    if countries:
        country = countries.first()
    else:
        country = models.Country (country=country_name)
        country.save()
    
    return country
        
def get_create_time_zone (time_zone_name:str):
    """ Return or create (if not exists) a time zone

    Args:
        time_zone_name (str): time zone name
        
    Returns:
        models.Country: country instance
    """
    
    time_zones = models.TimeZone.objects.filter(time_zone=time_zone_name)
    if time_zones:
        time_zone = time_zones.first()
    else:
        time_zone = models.TimeZone (time_zone=time_zone_name)
        time_zone.save()
    
    return time_zone

def clean_phone (phone:str):
    """ Clean extra chars from phone number

    Args:
        phone (str): input phone number

    Returns:
        str: clean phone number
    """
    
    clean_number = ""
    for char in phone:
        if char.isdigit():
            clean_number += char
    
    return clean_number

def get_bits (user:models.User):
    """ get the current bits of the user

    Args:
        user (models.User): user object

    Returns:
        querySet: querySet of the user bits
        int: current balance of the user
    """
    
    bits = models.Bit.objects.filter(user=user)
    bits_num = bits.aggregate(Sum('amount'))['amount__sum']
    
    if not bits_num:
        bits_num = 0
    
    return bits, bits_num