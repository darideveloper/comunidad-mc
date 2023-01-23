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

def get_user_points (user:models.User):
    """ Get user's points by (day, week and total)

    Args:
        user (models.User): instance of User model

    Returns:
        touple: (today_points:int, week_points:int, total_points:int)
    """
    
    # Calculate the last 7 days
    back_dates = [datetime.now() - timedelta(days=back_date) for back_date in range(1, 8)]

    week_points = 0
    total_points = 0

    # Get points of the current date
    today_points = models.Point.objects.filter(user=user, datetime__date=datetime.now().date()).count()
    
    # Calculate total points
    total_points += models.Point.objects.filter(user=user).count()

    # Get user's points by in ech back day
    for date in back_dates:
        day_points = models.Point.objects.filter(user=user, datetime__date=date).count()
        
        # Set max day points to 10
        if day_points > 10:
            day_points = 10
            
        # Add day points to week points
        week_points += day_points
        
    return today_points, week_points, total_points
