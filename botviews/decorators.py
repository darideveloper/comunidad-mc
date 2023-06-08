import os
from . import models
from functools import wraps
from django.http import HttpResponseBadRequest

DEBUG = os.getenv("DEBUG") == "True"


def validate_token (function):
    """ View wrapper for return data only if the token it's valid """
    
    @wraps(function)
    def wrap (request, *args, **kwargs):
        
        # Validate token
        token = request.GET.get ("token")
        token_found = models.Token.objects.filter (value=token)
        if token_found and token_found.first().is_active:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest ("Invalid token")
        
    return wrap