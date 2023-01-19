from . import models

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