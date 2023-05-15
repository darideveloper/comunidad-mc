import django
from . import decorators
from . import models
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone


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
def get_donations(request):
    """ Returns donations to the current streams in json format """
    
    # Get current hour with timezone
    hour = timezone.localtime(timezone.now()).hour
    
    # Get to do donations of the current hour
    donations = models.Donation.objects.filter(hour=hour, done=False, user__is_active=True)
    
    # Format data
    donations_formatted = []
    for donation in donations:
        donations_formatted.append ({
            "user": donation.user.name,
            "admin": donation.user.user_auth.username,
            "stream_chat_link": donation.stream_chat_link,
            "hour": donation.hour,
            "minute": donation.minute,
            "amount": donation.amount,
            "message": donation.message,
            "cookies": donation.user.cookies,
        })

    return JsonResponse(donations_formatted, safe=False)