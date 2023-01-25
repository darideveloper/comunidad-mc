from functools import wraps
from django.shortcuts import redirect

def validate_login (function):
    @wraps(function)
    def wrap (request, *args, **kwargs):
        if "user_id" in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect ("landing")
        
    return wrap
