import os
import json
import django
from dotenv import load_dotenv
from . import models
from app import models as app_models
from . import decorators
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from app.twitch import TwitchApi
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

# Load enviroment variables
DEBUG = os.getenv("DEBUG") == "True"

def get_json_model(model: django.db.models, get_objects=True) -> str:
    """ Serializes a model to json

    Args:
        model (django.db.models): model to serialize

    Returns:
        str: json data
    """

    # Get all objects from table
    if get_objects:
        objects = model.objects.all()
    else:
        objects = model

    # Format objects to json
    objects_json = serializers.serialize('json', objects)

    return objects_json


@decorators.validate_token
def get_settings(request):
    """ Returns all settings in json format """
    return HttpResponse(get_json_model(models.Setting), content_type='application/json')


@decorators.validate_token
def get_proxies(request):
    """ Returns all proxies in json format """

    return HttpResponse(get_json_model(models.Proxy), content_type='application/json')


@decorators.validate_token
def get_users(request):
    """ Returns all users in json format """

    return HttpResponse(get_json_model(models.User), content_type='application/json')


@decorators.validate_token
def get_locations(request):
    """ Returns all locations in json format """

    return HttpResponse(get_json_model(models.Location), content_type='application/json')


@decorators.validate_token
def get_streams(request):
    """ Returns names of the current streamers in comunidad mc, as json format """

    # get current streams
    twitch = TwitchApi("Views BotViews")
    streams = twitch.get_current_streams()

    # Get streamers
    streamers = []
    if streams:
        streamers = list(map(lambda stream: stream.user.user_name, streams))

    # Return always one stream in debug mode
    if not streamers and DEBUG:
        streamers = ["darideveloper"]

    return JsonResponse(streamers, safe=False)

@decorators.validate_token
def disable_user (request, name:str):
    """ Set user is_active status to False, to specific user

    Args:
        name (str): name of the user to disable
    """
    
    user = models.User.objects.get(name=name)
    user.is_active = False
    user.save()
    
    return HttpResponse("User disabled")

@decorators.validate_token
def get_proxy(request):
    """ Returns random proxy in json format """

    # Get random proxy
    proxy = models.Proxy.objects.order_by('?').first()
    
    # Empry data by default
    proxy_formatted = {
        "host": "",
        "port": "",
    }

    # Update data
    if proxy:
        proxy_formatted["host"] = proxy.host
        proxy_formatted["port"] = proxy.port

    return JsonResponse({
        "proxy": proxy_formatted,
    }, safe=False)    

@decorators.validate_token
@csrf_exempt
def update_cookies(request, name):
    """ Update cookies from specific user """
    
    # Get user by name 
    user = models.User.objects.filter(name=name)
    if not user: 
        # Return error if user not found
        return JsonResponse({
            "status": "error",
            "message": "User not found"    
        }, safe=False)
    
    
    # Get json data
    json_data = json.loads(request.body)
    
    # Validate cookies inside json
    if not "cookies" in json_data:
        # Return error if cookies not found
        return JsonResponse({
            "status": "error",
            "message": "Cookies not found"    
        }, safe=False)
    
    # Activate user
    user = user[0]
    user.is_active = True
    
    # Update cookies
    user.cookies = json_data["cookies"]
    
    # Save user
    user.save()
    
    return JsonResponse({
        "status": "ok",
        "message": "Cookies updated" 
    })