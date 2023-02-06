from functools import wraps
from django.shortcuts import redirect
from .tools import get_user_message_cookies

def validate_login (function):
    """ View wrapper for show page only if user is logged in. """
    @wraps(function)
    def wrap (request, *args, **kwargs):
        if "user_id" in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect ("landing")
        
    return wrap

def validate_whatsapp (function):
    """ View wrapper for show page only if user have been validated whatsapp. """
    @wraps(function)
    def wrap (request, *args, **kwargs):
        user, other = get_user_message_cookies(request)
        if user.is_active:
            return function(request, *args, **kwargs)
        else:
            return redirect ("whatsapp")
        
    return wrap