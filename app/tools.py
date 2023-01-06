import datetime
import threading
from django.utils import timezone
import requests
from . import models

def submit_streams_node_bg (node_api:str): 
    """ run funtion "submit_streams_node" in background with threads

    Args:
        node_api (str): url of node.js api
    """
    
    # Create thread and start it
    thread_obj = threading.Thread(target=submit_streams_node, args=(node_api,))
    thread_obj.start()

def submit_streams_node (node_api:str):
    """ Submit streams to node.js api for start reading comments

    Args:
        node_api (str): url of node.js api

    Returns:
        bool: True if node.js api is working, False if not
    """
    
    node_error = False
    
    # Get date ranges
    now = timezone.now()
    start_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, 0, 0, tzinfo=timezone.utc)
    end_datetime = datetime.datetime(now.year, now.month, now.day, now.hour, 59, 59, tzinfo=timezone.utc)
        
    # Get current stream
    streams_data = {
        "streams": []
    }
    current_streams = models.Stream.objects.filter(datetime__range=[start_datetime, end_datetime]).all()
    for stream in current_streams:
        # Get and stremer data
        streams_data["streams"].append ({
            "access_token": stream.user.access_token,
            "user_name": stream.user.user_name,
            "stream_id": stream.id,
        })  
        
    # Send data to node.js api for start readding comments, and catch errors
    try:
        res = requests.post(node_api, json=streams_data)
        res.raise_for_status()
    except:        
        node_error = True
        
    return node_error