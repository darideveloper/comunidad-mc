from . import models
from datetime import datetime, timedelta

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
    """ Get user point and return them """
    
    # get points
    general_points = models.GeneralPoint.objects.filter(user=user).order_by("datetime").reverse()
    weekly_points = models.WeeklyPoint.objects.filter(general_point__user=user)
    daily_points = models.DailyPoint.objects.filter(general_point__user=user)
    
    return general_points, weekly_points, daily_points
    