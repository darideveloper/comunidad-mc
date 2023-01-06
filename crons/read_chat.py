# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

from app.tools import submit_streams_node
from dotenv import load_dotenv

# Load and get credentials
load_dotenv ()
NODE_API = os.environ.get("NODE_API")

# Submit data to nodejs api, for start reading chat
submit_streams_node(NODE_API)