import json
import requests
from .logs import logger


def get_tokens(client_id: str, client_secret: str, login_code: str, direct_url: str):
    """ Get tokens from twitch api, at the endpoint: https://id.twitch.tv/oauth2/token

    Args:
        client_id (str): twitch client id
        client_secret (str): twitch client secret
        login_code (str): code generated by twitch after login
        direct_url (str): url who twitch redirect after login

    Returns:
        tuple: access_token, refresh_token
    """

    # Get twitch token for ganarate login url
    token_url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": login_code,
        "grant_type": "authorization_code",
        "redirect_uri": direct_url,
    }
    res = requests.post(token_url, data=params)
    json_data = json.loads(res.content)
    logger.debug (str(json_data))

    # Extract variables
    access_token = json_data.get("access_token", "")
    refresh_token = json_data.get("refresh_token", "")
    logger.debug (f"{access_token}, {refresh_token}")
    return (access_token, refresh_token)


def get_user_info(user_token: str):
    """ Get user information using user access token

    Args:
        user_token (str): token of the user already logged to the app

    Returns:
        tuple: user_id, user_email, user_picture, user_name
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token}"
    }

    res = requests.get("https://id.twitch.tv/oauth2/userinfo", headers=headers)
    json_data = json.loads(res.content)
    user_id = json_data.get("sub", "")
    user_email = json_data.get("email", "")
    user_picture = json_data.get("picture", "")
    user_name = json_data.get("preferred_username", "")

    return (user_id, user_email, user_picture, user_name)


def get_twitch_login_link(client_id: str, redirect_url: str):
    """ Generate link for login with twitch

    Args:
        client_id (str): twitch client id
        redirect_url (str): url to redirect after login

    Returns:
        str: twitch login link
    """

    # Generate link
    url_params = {
        "client_id": client_id,
        "redirect_uri": redirect_url,
        "response_type": "code",
        "force_verify": "true",
        "scope": "openid user:read:email moderation:read moderator:read:chatters moderator:read:chat_settings chat:read",
        "state": "sample_string",
        "claims": '{"userinfo":{"picture":null, "email":null, "name":null, "user": null, "preferred_username": null}}'
    }
    encoded_params = "&".join(
        [f"{param_key}={param_value}" for param_key, param_value in url_params.items()])
    twitch_link = f"https://id.twitch.tv/oauth2/authorize?{encoded_params}"

    return twitch_link

def get_users_in_chat (user_id: int, user_token: str, client_id: str):
    """ Get list of users in chat of a stream

    Args:
        user_id (int): user if of streamer
        user_token (str): user token of the streamer
        client_id (str): client id of the app

    Returns:
        list: id of users in chat
    """
    
    url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Client-Id": client_id
    }
    res = requests.get(url, headers=headers)
    json_data = res.json()
    
    if not json_data:
        return False
    
    users_active = list(map(lambda user: user["user_id"], json_data["data"]))
    return users_active