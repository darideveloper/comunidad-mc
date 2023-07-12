# Update all users tokens if is invalid
import requests

# Add parent folder to path
import os
import sys
from time import sleep
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models
from app.twitch import TwitchApi
from django.core.mail import send_mail

log_origin_name = "Update Tokens"
log_origin = models.LogOrigin.objects.get (name=log_origin_name)
log_type_error = models.LogType.objects.get (name="error")
try:
    twitch = TwitchApi (log_origin_name)

    users = models.User.objects.all()

    errors = []
    counters = {
        "error": 0,
        "ok": 0
    }
    for user in users:
        
        # Loop for update token if is invalid
        error = ""
        for _ in range (2):

            user_id = user.id
            user_token = user.access_token
            url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
            headers = {
                "Authorization": f"Bearer {user_token}",
                "Client-Id": "p1yxg1ystvc7ikxem39q7mhqq9fk59" # twitch client id from .env
            }
            res = requests.get(url, headers=headers)
            json_data = res.json()
            
            if "data" in json_data:
                error = ""
                break
            
            # Auto update user token
            if "message" in json_data:
                message = json_data["message"]
                error = message
                twitch.update_token (user)
                
            sleep (10)
            
        if error:
            errors.append ({
                "message": f"user {user}: {error}",
                "email": user.email,
                "name": user.user_name
            })
            counters["error"] += 1
        else:
            counters["ok"] += 1
    
    models.Log.objects.create (
        origin=log_origin,
        details=f"Summary: {counters['ok']} updated, {counters['error']} errors",
    )
 
    models.Log.objects.create (
        origin=log_origin,
        details=f"Details: ",
    )
    
    for error in errors:
        
        # Log invalid tokens
        models.Log.objects.create (
            origin=log_origin,
            details=error["message"],
        )
        
        # Submit email to each user
        body = f"Hola, {error.name}"
        body = "\nSe ha detectado poca actividad en tu cuenta de Comunidad MC, vinculada a deste correo"
        body += "\nPara evitar que tu cuenta sea inhabilitada, ingresa a la pagina de Comunidad MC y actualiza tus datos desde la página de perfil:"
        body += "\nhttps://comunidadmc.com/profile/"
        body += "\n\nSi es la primera vez que recibes este mensaje, no es necesario crear un ticket de soporte."
        body += "\n\nAtentamente, Dari Dev, administrador de Comunidad MC"
        
        
        send_mail(
            "Aviso de baja actividad en tu cuenta de ComunidadMC",
            body,
            "darideveloper@gmail.com",
            [error.email],
            fail_silently=False,
        ) 
        

except Exception as e:
    log_type_error = models.LogType.objects.get (name="error")
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )
    