# Test to get checks from specific user
import requests

user_id = 769435763 # user id
user_token = "cox3ycfx5cnp1hbrlr3wup6z6i6lui" # user access token
url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
headers = {
    "Authorization": f"Bearer {user_token}",
    "Client-Id": "p1yxg1ystvc7ikxem39q7mhqq9fk59" # twitch client id from .env
}
res = requests.get(url, headers=headers)
json_data = res.json()
print (json_data)