from functools import wraps
from django.shortcuts import redirect
from . import tools

def validate_login (function):
    """ View wrapper for show page only if user is logged in. """
    @wraps(function)
    def wrap (request, *args, **kwargs):
        user, *other = tools.get_cookies_data(request, delete_data=False)
        if user:
            return function(request, *args, **kwargs)
        else:
            return redirect ("landing")
        
    return wrap

def validate_login_active (function):
    """ View wrapper for show page only if user have been validated by whatsapp. """
    @wraps(function)
    def wrap (request, *args, **kwargs):
        user, *other = tools.get_cookies_data(request, delete_data=False)
        if user and user.is_active:
            return function(request, *args, **kwargs)
        else:
            return redirect ("home")
        
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