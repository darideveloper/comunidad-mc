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
    
    # Get today donations of the current hour
    donations = models.Donation.objects.filter(
        datetime__time__hour=hour, 
        done=False, 
        user__is_active=True,
        datetime__date= timezone.localtime(timezone.now()).date()
    )
                                               
    # Format data
    donations_formatted = []
    for donation in donations: 
        donations_formatted.append ({
            "id": donation.id,
            "user": donation.user.name,
            "admin": donation.user.user_auth.username,
            "stream_chat_link": donation.stream_chat_link,
            "time": timezone.localtime(donation.datetime).time(),
            "amount": donation.amount,
            "message": donation.message,
            "cookies": donation.user.cookies,
        })

    return JsonResponse(donations_formatted, safe=False)

@decorators.validate_token
def disable_user (request, name:str):
    """ Set is_active status to False, to specific user

    Args:
        name (str): name of the user to disable
    """
    
    user = models.User.objects.filter (name=name)
    if user:
        user = user[0]
        user.is_active = False
        user.save()
        
        return HttpResponse("User disabled")
    
    else:
        return HttpResponse("User not found")
    

@decorators.validate_token
def upodate_donation (request, id:int):
    """ Set done status to True, to specific donation

    Args:
        id (int): donation id
    """
    
    donation = models.Donation.objects.filter (id=id)
    if donation:
        donation = donation[0]
        donation.done = True
        donation.save()
        
        return HttpResponse("Donation updated")
    
    else:
        return HttpResponse("Donation not found")