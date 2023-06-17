import django
from . import decorators
from . import models
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

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
        donation = donation[0]
        donation.done = True
        donation.save()

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
        })
        
    return JsonResponse({
        "users": users_formatted    
    }, safe=False)
    