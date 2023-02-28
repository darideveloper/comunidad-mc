from . import models
from . import tools
import requests as req
from .logs import logger
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta

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
    """ get user and fix profile image if not exist """
    
    user_picture = user.picture
    valid_picture = True
    
    if not "static" in user_picture:
        
        # Try to get image from url
        try:
            res = req.get (user_picture)
        except:
            valid_picture = False
        else:        
            if not res.status_code == 200:
                valid_picture = False
        
        # Use profile image if error
        if not user_picture or not user_picture.endswith(".jpg") or not valid_picture:
            user.picture = "/static/app/imgs/profile.png"
            user.save()
            
    # Return user with new profile image
    return user

def get_cookies_data (request, delete_data:bool=True):
    
    """ Get user and message from cookies

    Returns:
        touple: user object, menssaje text, error text
    """

    # Get user data from cookies
    user_id = request.session.get("user_id", 0)
    users = models.User.objects.filter(id=user_id)
    
    # Delete cookies if user not exist and return None
    if users.count() == 0:
        print (users)
        try:
            del request.session[user_id]
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
    
def get_general_points (user):
    """ Return the general points (registers and counters) from specific user """
    general_points = models.GeneralPoint.objects.filter(user=user).order_by("datetime").reverse()
    general_points_num = general_points.aggregate(Sum('amount'))['amount__sum']
    
    if not general_points_num:
        general_points_num = 0
    
    return general_points, general_points_num
    
def get_user_points (user):
    """ Get user point, count and register reguister and counters """
    
    # General points
    general_points, general_points_num = get_general_points(user)
    
    # get points registers
    weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user)
    daily_points = models.DailyPoint.objects.filter(general_point__user=user)
    
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
     
def get_user_streams (user, user_time_zone):
    """ Return user streams for the next 7 days, and its proccessed data

    Args:
        user (models.User): user instance

    Returns:
        touple: user_streams (model Objects), user_streams_data (array)
    """
    
    logger.debug (f"Getting next streams of the user {user}")
    now = timezone.now()
    start_datetime = datetime(
        now.year, now.month, now.day, now.hour, 0, 0, tzinfo=timezone.utc)
    end_datetime = start_datetime + timedelta(days=7)

    # Get current streams
    user_streams = models.Stream.objects.filter(
        datetime__range=[start_datetime, end_datetime], user=user).all().order_by("datetime")
    
    if not user_streams:
        user_streams = []
        
    # Format streams
    user_streams_data = []
    for stream in user_streams:
        id = stream.id
        stream_datetime = stream.datetime.astimezone(user_time_zone)
        date = stream_datetime.strftime("%Y-%m-%d")
        time = stream_datetime.strftime("%I:%M %p")
        hour = stream_datetime.strftime("%H")
        is_cancellable = is_stream_cancelable(stream)
        user_streams_data.append ({
            "id": id,
            "date": date, 
            "time": time, 
            "is_cancellable": "regular" if is_cancellable else "warning",
            "hour": hour,
        })
        
    return user_streams, user_streams_data

def is_stream_cancelable (stream):
    """ Return if stream is cancelable or not

    Args:
        stream (models.Stream): stream object

    Returns:
        bool: True if stream is cancelable, False if not
    """
    
    return stream.datetime > ( timezone.now() + timedelta(hours=1) )

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
    general_points = models.GeneralPoint.objects.filter (user=user, info=info_point, stream=stream)
    if general_points:
        
        # Incress negative point
        general_point = general_points.first()
        general_point.amount -= amount
        general_point.save()
        
    else:
                
        # Add new point
        general_point = models.GeneralPoint (user=user, datetime=timezone.now(), amount=-amount, info=info_point, stream=stream)
        general_point.save ()
    
    return True
    