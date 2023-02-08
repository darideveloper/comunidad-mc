from functools import wraps
from django.shortcuts import redirect
from . import tools

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
        user, *other = tools.get_cookies_data(request, delete_data=False)
        if user.is_active:
            return function(request, *args, **kwargs)
        else:
            return redirect ("whatsapp")
        
    return wrap

def validate_admin (function):
    """ Validate if user is admin, for show page """
    @wraps(function)
    def wrap (request, *args, **kwargs):
        user, *other = tools.get_cookies_data(request, delete_data=False)
        if user.admin_type:
            return function(request, *args, **kwargs)
        else:
            return redirect ("support")
        
    return wrap