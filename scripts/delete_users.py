# Delete specific users

# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()
from app import models

users = [
    "aaronplays_gt",
    "aitor0311_",
    "AlfreddOh",
    "AruBoa",
    "azzizxj",
    "bad_zopas",
    "bannedyaiza_",
    "brochin_gamer_gt",
    "darth_santiago",
    "ElCompaElvis",
    "ELNIOFINO",
    "fachero_ult",
    "greenarrow_1980",
    "hachero0899",
    "ivan_rico22",
    "jesusilv13",
    "JoeTDK",
    "josepo_gg",
    "Kiropollo",
    "kirssita",
    "KpopFanMusic",
    "LitoXR",
    "naciionalero",
    "poderosogato",
    "principerhodesia",
    "ragnar27_",
    "richyn_twitch",
    "salmeroonx",
    "soyunfarsantee",
    "spek25",
    "stanchmage",
    "taro1094",
    "tecno730",
    "tortsquad",
    "tureko5",    
    "voltagamingyt",
    "zovalenplay"
]

for user in users:
    print (f"Deleting user {user}")
    user_obj = models.User.objects.filter(user_name=user).first()
    user_obj.delete()