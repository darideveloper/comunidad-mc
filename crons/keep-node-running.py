# Send query to node js to keep server running
import requests
import os
from dotenv import load_dotenv

load_dotenv ()
NODE_API = os.getenv('NODE_API')

res = requests.get (NODE_API)
res.raise_for_status ()