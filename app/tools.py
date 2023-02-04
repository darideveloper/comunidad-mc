from . import models
from datetime import datetime, timedelta
from django.db.models import Sum

def get_user_message_cookies (request):
    
    """ Get user and message from cookies

    Returns:
        touple: message and user
    """

    # Get user data from cookies
    user_id = request.session["user_id"]
    user = models.User.objects.filter(id=user_id).first()
    
    # Get message from cookies
    message = request.session.get("message", "")
    if message:
        del request.session["message"]
    
    return user, message
    
def get_user_points (user):
    """ Get user point, count and register reguister and counters """
    
    # get points registers
    general_points = models.GeneralPoint.objects.filter(user=user).order_by("datetime").reverse()
    weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user)
    daily_points = models.DailyPoint.objects.filter(general_point__user=user)
    
    # Calculate sums of points
    general_points_num = general_points.aggregate(Sum('amount'))['amount__sum']
    weekly_points_num = weekly_points.aggregate(Sum('general_point__amount'))['general_point__amount__sum']
    daily_points_num = daily_points.aggregate(Sum('general_point__amount'))['general_point__amount__sum']
    
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
     