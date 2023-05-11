import os
import django
from dotenv import load_dotenv
from . import models
from . import decorators
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from app.twitch import TwitchApi

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
    twitch = TwitchApi()
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
def get_donations(request):
    """ Returns donations to the current streams in json format """

    # get current streams
    twitch = TwitchApi()
    streams = twitch.get_current_streams()
    
    # Get donations from current streams
    donations = models.Donation.objects.filter(stream__in=streams)
    
    # Format data
    donations_formatted = []
    for donation in donations:
        donations_formatted.append ({
            "user": donation.user.name,
            "streamer": donation.stream.user.user_name,
            "minute": donation.minute,
            "amount": donation.amount,
            "message": donation.message,
            "status": donation.status,
        })

    return JsonResponse(donations_formatted, safe=False)
