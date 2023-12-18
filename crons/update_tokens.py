# Update all users tokens if is invalid
import requests

# Add parent folder to path
import os
import sys
from dotenv import load_dotenv
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
from django.utils import timezone

load_dotenv()

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")

log_origin_name = "Update Tokens"
log_origin = models.LogOrigin.objects.get (name=log_origin_name)
log_type_error = models.LogType.objects.get (name="error")
log_type_info = models.LogType.objects.get (name="info")

# Get current streams
twitch = TwitchApi (log_origin_name)
streams = twitch.get_current_streams()
streamers = [stream.user for stream in streams]

# Get current datetime od the time zone
now = timezone.now()

try:

    user = None
    while True: 

        # Get oldest updated user
        user = models.User.objects.filter(is_active=True).order_by("last_update_token").first()
        
        # Skip streamers
        if not user in streamers:
            break  
               
    # Loop for update token if is invalid
    error = ""
    for _ in range (2):

        user_id = user.id
        user_token = user.access_token
        url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Client-Id": TWITCH_CLIENT_ID
        }
        res = requests.get(url, headers=headers)
        json_data = res.json()
        
        if "data" in json_data:
            error = ""
            break
        
        # Auto update user token
        if "message" in json_data:
            message = json_data["message"]
            error = f"Token update requiered for user {user.user_name} ({message})"
            
            # Log invalid tokens
            models.Log.objects.create (
                origin=log_origin,
                details=error,
            )
            
            # Update token
            twitch.update_token (user)
            
        sleep (10)
    
    if error:
        
        if user.send_mail:        
                
            # Submit email to user
            body = f"Hola, {user.user_name}"
            body = "\nSe ha desvinculado tu cuenta de Twitch de Comunidad MC, relacionada a deste correo"
            body = "\n¿Por qué sucedió esto?"
            body = "\nPuede ser por baja actividad en nuestra plataforma, configuraciones que hayas realizado en tu cuenta de Twitch, actualizaciones de Twitch o por un error en nuestro sistema."
            body += "\n\nPara evitar que tu cuenta sea inhabilitada, o reibas penalizaaciones realiza lo siguiente:"
            body += "\n\n1. Ve a Comunidad MC"
            body += "\n2. Cierra sesión"
            body += "\n3. Inicia sesión nuevamente, con tu misma cuenta de twitch"
            body += "\n4. Actualiza tus datos desde la página de perfil."
            body += "\n\nSi es la primera vez que recibes este mensaje, *no es necesario crear un ticket de soporte*."
            body += "\n\nAtentamente, Dari Dev, administrador de Comunidad MC"
            
            # Try to send email and save final status
            try:
                send_mail(
                    "Aviso de desvinculación de cuenta de ComunidadMC",
                    body,
                    "darideveloper@gmail.com",
                    [user.email],
                    fail_silently=False,
                ) 
            except:
                models.Log.objects.create (
                    origin=log_origin,
                    details=f"Error sending email to user {user.user_name}",
                )
            else:
                models.Log.objects.create (
                    origin=log_origin,
                    details=f"Email sent to user {user.user_name}",
                )

        user.update_tries += 1
        
        # Deactivate user if has 3 tries
        if user.update_tries >= 3:
            user.is_active = False
        
    else:
        # Log valid token
        models.Log.objects.create (
            origin=log_origin,
            details=f"Token updated for user {user.user_name}",
            log_type=log_type_info
        )
        
    # Update user data
    user.last_update_token = now
    user.save ()
        

except Exception as e:
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )
    