from . import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from app.twitch import TwitchApi

def get_settings (request):
    
    # Get all settings from table
    settings = models.Setting.objects.all()
    
    # Format settings to json
    settings_json = serializers.serialize('json', settings)
        
    return HttpResponse(settings_json, content_type='application/json')

def get_proxies (request):
    
    # Get all proxies from table
    proxies = models.Proxy.objects.all()
    
    # Format proxies to json
    proxies_json = serializers.serialize('json', proxies)
        
    return HttpResponse(proxies_json, content_type='application/json')

def get_users (request):
    
    # Get all users from table
    users = models.User.objects.all()
    
    # Format users to json
    users_json = serializers.serialize('json', users)
        
    return HttpResponse(users_json, content_type='application/json')

def get_locations (request):
    
    # Get all locations from table
    locations = models.Location.objects.all()
    
    # Format locations to json
    locations_json = serializers.serialize('json', locations)
    
    return HttpResponse(locations_json, content_type='application/json')
    
def get_streams (request):
    
    # get current streams
    twitch = TwitchApi()
    streams = twitch.get_current_streams ()
    
    # Get streamers
    streamers = list(map(lambda stream: stream.user.user_name, streams))
    data_json = {"streams": streamers}
        
    return JsonResponse (data_json)