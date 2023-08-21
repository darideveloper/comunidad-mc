import json
from . import decorators
from . import models
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app import models as app_models

logs_origin = app_models.LogOrigin.objects.get(name="BotCheers")
logs_type_info = app_models.LogType.objects.get(name="info")
logs_type_error = app_models.LogType.objects.get(name="error")

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
        datetime__date=timezone.localtime(timezone.now()).date()
    )

    # Format data
    donations_formatted = []
    for donation in donations:
        donations_formatted.append({
            "id": donation.id,
            "user": donation.user.name,
            "admin": donation.user.user_auth.username,
            "stream_chat_link": donation.stream_chat_link,
            "time": timezone.localtime(donation.datetime).time(),
            "amount": donation.amount,
            "message": donation.message,
            "cookies": donation.user.cookies,
        })

    return JsonResponse({
        "donations": donations_formatted,
    }, safe=False)


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
def disable_user(request, name: str):
    """ Set is_active status to False, to specific user

    Args:
        name (str): name of the user to disable
    """

    user = models.User.objects.filter(name=name)
    if user:
        user = user[0]
        user.is_active = False
        user.save()

        return HttpResponse("User disabled")

    else:
        return HttpResponse("User not found")


@decorators.validate_token
def upodate_donation(request, id: int):
    """ Set done status to True, to specific donation

    Args:
        id (int): donation id
    """

    donation = models.Donation.objects.filter(id=id)
    if donation:
         
        # Update donation status
        donation = donation[0]
        donation.done = True
        donation.save()
        
        # Validate claimed bits
        bits_app = donation.bits_app
        if bits_app:
            bits_app.is_bits_done = True
            bits_app.save ()
            
        return HttpResponse("Donation updated")

    else:
        return HttpResponse("Donation not found")



@decorators.validate_token
def get_users(request):
    """ Returns all user names and passwords in json format """

    # Get all users
    users = models.User.objects.all()
    
    # Formmat only username and password
    users_formatted = []
    for user in users:
        users_formatted.append ({
            "username": user.name,
            "password": user.password,
            "is_active": user.is_active,
        })
        
    return JsonResponse({
        "users": users_formatted    
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