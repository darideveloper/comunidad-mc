import os
import pytz
import json
import requests
import datetime
import threading
from . import models
from time import sleep
from .logs import logger
from dotenv import load_dotenv
from django.utils import timezone

class TwitchApi:

    def __init__(self):
        # Load and get credentials
        load_dotenv ()
        self.node_api = os.environ.get("NODE_API")
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_secret = os.getenv("TWITCH_SECRET")
        self.min_checks = int(os.getenv("MIN_CHECKS"))
        self.min_comments = int(os.getenv("MIN_COMMENTS"))
        self.max_daily_points = int(os.getenv("MAX_DAILY_POINTS"))
        self.wait_minutes_points = int(os.getenv("WAIT_MINUTES_POINTS"))

    def get_current_streams(self):
        """ Get the current live streams from databse

        Returns:
            models.Stream.objects: Streams instances
        """

        # Get date ranges
        logger.debug ("Getting streams from database for current hour")
        now = timezone.now()
        start_datetime = datetime.datetime(
            now.year, now.month, now.day, now.hour, 0, 0, tzinfo=timezone.utc)
        end_datetime = datetime.datetime(
            now.year, now.month, now.day, now.hour, 59, 59, tzinfo=timezone.utc)

        # Get current streams
        current_streams = models.Stream.objects.filter(
            datetime__range=[start_datetime, end_datetime]).all()
        
        if not current_streams:
            logger.info("No streams found")
            return []
        
        return current_streams
    

    def submit_streams_node_bg(self):
        """ run funtion "submit_streams_node" in background with threads

        Args:
            self.node_api (str): url of node.js api
        """

        # Create thread and start it
        logger.info("Starting thread for submit streams to node.js api")
        thread_obj = threading.Thread(
            target=self.submit_streams_node)
        thread_obj.start()


    def submit_streams_node(self):
        """ Submit streams to node.js api for start reading comments

        Args:
            self.node_api (str): url of node.js api

        Returns:
            bool: True if node.js api is working, False if not
        """

        node_error = False
        current_streams = self.get_current_streams()
        if not current_streams:
            return None
        
        streams_data = {"streams": []}
        for stream in current_streams:
            # Get and stremer data
            streams_data["streams"].append({
                "access_token": stream.user.access_token,
                "user_name": stream.user.user_name,
                "stream_id": stream.id,
            })
            
        if not streams_data:
            return None

        # Send data to node.js api for start readding comments, and catch errors
        try:
            logger.info("Sending streams to node.js api")
            res = requests.post(self.node_api, json=streams_data)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"Error sending streams to node.js api: {e}")
            node_error = True

        return node_error


    def is_node_working(self):
        """ Submit a basic request to node.js api to check if is working

        Args:
            self.node_api (str): url of node.js api

        Returns:
            bool: True if node.js api is working, False if not
        """

        logger.info("Checking if node.js api is working")
        try:
            res = requests.post(self.node_api)
        except Exception as e:
            logger.error(f"Error checking if node.js api is working: {e}")
            return False
        else:
            return True


    def get_tokens(self, login_code: str, direct_url: str):
        """ Get tokens from twitch api, at the endpoint: https://id.twitch.tv/oauth2/token

        Args:
            login_code (str): code generated by twitch after login
            direct_url (str): url who twitch redirect after login

        Returns:
            tuple: access_token, refresh_token
        """

        # Get twitch token for ganarate login url
        token_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_secret,
            "code": login_code,
            "grant_type": "authorization_code",
            "redirect_uri": direct_url,
        }
        res = requests.post(token_url, data=params)
        json_data = json.loads(res.content)
        logger.debug(str(json_data))

        # Extract variables
        access_token = json_data.get("access_token", "")
        refresh_token = json_data.get("refresh_token", "")
        logger.debug(f"{access_token}, {refresh_token}")
        return (access_token, refresh_token)


    def get_user_info(self, user_token: str):
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

        res = requests.get(
            "https://id.twitch.tv/oauth2/userinfo", headers=headers)
        json_data = json.loads(res.content)
        user_id = json_data.get("sub", "")
        user_email = json_data.get("email", "")
        user_picture = json_data.get("picture", "")
        user_name = json_data.get("preferred_username", "")

        return (user_id, user_email, user_picture, user_name)

    def get_twitch_login_link(self, redirect_url: str):
        """ Generate link for login with twitch

        Args:
            redirect_url (str): url to redirect after login

        Returns:
            str: twitch login link
        """

        # Generate link
        twitch_scope = [
            "openid",
            "user:read:email",
            "moderation:read",
            "moderator:read:chatters",
            "moderator:read:chat_settings",
            "chat:read",
            "bits:read",
        ]
        url_params = {
            "client_id": self.twitch_client_id,
            "redirect_uri": redirect_url,
            "response_type": "code",
            "force_verify": "true",
            "scope": " ".join(twitch_scope),
            "state": "sample_string",
            "claims": '{"userinfo":{"picture":null, "email":null, "name":null, "user": null, "preferred_username": null}}'
        }
        encoded_params = "&".join(
            [f"{param_key}={param_value}" for param_key, param_value in url_params.items()])
        twitch_link = f"https://id.twitch.tv/oauth2/authorize?{encoded_params}"

        return twitch_link


    def check_users_in_chat(self):
        """ Get list of users in chat of the current streams and save in databse """
        
        # Get current streams and loop  
        current_streams = self.get_current_streams ()
        if not current_streams:
            return None
        
        for stream in current_streams:
            
            # Loopf ror get data and update token
            while True:
                
                # Get current stream
                streamer = stream.user
                    
                # Request data
                user_id = streamer.id
                user_token = streamer.access_token
                url = f"https://api.twitch.tv/helix/chat/chatters?broadcaster_id={user_id}&moderator_id={user_id}"
                headers = {
                    "Authorization": f"Bearer {user_token}",
                    "Client-Id": self.twitch_client_id
                }
                res = requests.get(url, headers=headers)
                json_data = res.json()

                if not json_data:
                    continue
                
                # Validate if token is expired and retry
                if "error" in json_data:
                    self.update_token(streamer)         
                    continue
                else:
                    break       

            # Get users in chat
            users_active = list(map(lambda user: user["user_id"], json_data.get("data", [])))
        
            # Filter only user who exist in database
            valid_users = models.User.objects.filter(id__in=users_active)
            if len(valid_users) == 1:
                logger.info (f"No users in stream: {stream}")
            
            # Save in each watch in database
            for user in valid_users:
                
                # Skip if user is the streamer
                if user.id == streamer.id:
                    continue
                
                # Save check in database
                new_check = models.WhatchCheck(stream=stream, user=user)
                new_check.save ()
                logger.info (f"Check saved. User: {user}, Stream: {stream}")
                
                # Try to add point to user
                self.add_point(user, stream)


    def get_new_user_token(self, refresh_token: str):
        """ Update user token

        Args:
            refresh_token (str): refresh token of the userç

        Returns: 
            str: new access token
        """

        # Get new token
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.twitch_client_id,
            "client_secret": self.twitch_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        res = requests.post(url, data=params)
        if res.status_code != 200:
            logger.error(
                f"Error updating user refresh_token: ({res.status_code}) refresh_token")
            return ""

        json_data = res.json()
        access_token = json_data.get("access_token", "")
        if not access_token:
            logger.error(
                f"Error updating user refresh_token: ({res.status_code}) refresh_token")
            return ""

        return access_token
    
    def update_token (self, user: models.User):
        """ Update user token and save in database

        Args:
            user (models.User): user instance

        Returns: 
            bool: True if token updated, False if error
        """
            
        # Get new access token using refresh token  
        new_access_token = self.get_new_user_token(user.refresh_token)
        if not new_access_token:
            logger.error (f"Error generating new token for user: {user}")
            return False

        # Update user token
        user.access_token = new_access_token
        user.save()
        logger.info (f"User token updated: {user}")
        return True

    def add_point (self, user: models.User, stream: models.Stream = None):
        """ Add point to user after watch stream and comment in chat

        Args:
            user (models.User): user instance
            stream (models.Stream, optional): stream instance. Defaults to None.           
        """

        # Get live streams where no stream spificied
        current_streams = [stream]
        if not stream: 
            current_streams = self.get_current_streams ()
        
        # Loop for ech stream
        for stream in current_streams:

            # Get users whatch checks
            user_checks = models.WhatchCheck.objects.filter(user=user, stream=stream, status=1)
            
            # Get users comments
            user_comments = models.Comment.objects.filter(user=user, stream=stream, status=1)
            
            # Validate min number of checks and comments
            if len(user_checks) >= self.min_checks and len(user_comments) >= self.min_comments:
                
                # Subtract point to streamer (except rankings: diamente, platino and free streams)
                streamer = stream.user
                if streamer.admin_type and not stream.is_free:
                    info_point = models.InfoPoint.objects.get (info="viwer asistió a stream")
                    general_point = models.GeneralPoint (
                        user=streamer, stream=stream, datetime=timezone.now(), amount=-1, info=info_point)
                    general_point.save ()
                
                # Calculate time for stream ends
                stream_datetime = stream.datetime
                now = timezone.now ()
                wait_minutes = stream_datetime + timezone.timedelta(minutes=60 + self.wait_minutes_points) - now
                wait_seconds = wait_minutes.total_seconds()
                
                # Add point in background
                logger.info (f"Starting thread to add point to user {user}. Waiting time: {int(wait_seconds)} seconds")
                thread_obj = threading.Thread(target=self.add_point_bg, args=(user, stream, wait_seconds))
                thread_obj.start ()
                
                # Set done status to comments and checks
                done_status = models.Status.objects.get(id=2)
                for check in user_checks:
                    check.status = done_status
                    check.save ()
                    
                for comment in user_comments:
                    comment.status = done_status
                    comment.save ()
                        
    def add_point_bg (self, user:models.User, stream:models.Stream, wait_time:int):
        """ Add point in background using threads 
        
        Args:
            user (models.User): user instance
            stream (models.Stream): stream instance.
            wait_time (int): wait time in seconds before add point 
        """
        
        sleep (wait_time)
        
        logger.info(f"Added general point to user: {user}")
        
        # Save general point
        new_general_point = models.GeneralPoint (user=user, stream=stream)
        new_general_point.save ()
        
        # Validate if the user have less than the max number of daily points
        current_daily_points = models.DailyPoint.objects.filter(general_point__user=user).count()
        if current_daily_points < self.max_daily_points:
            
            # Save daily point
            new_daily_point = models.DailyPoint (general_point=new_general_point)
            new_daily_point.save()
            
            # save weekly point
            new_weekly_point = models.WeeklyPoint (general_point=new_general_point)
            new_weekly_point.save()
            
            logger.info(f"Added daily and weekly point to user: {user}")
            
            # Check if there are less than 10 users in the Ranking of daily points and if user already have 10 points
            current_tops = models.TopDailyPoint.objects.all().count()
            current_points = current_daily_points + 1
            if current_tops < 10 and current_points == 10:
                
                # Add user to Ranking of daily points if there isnt in table
                user_in_top = models.TopDailyPoint.objects.filter(user=user).count()
                if user_in_top == 0:
                    logger.info (f"User {user} already have 10 points. Added to Ranking of daily points")      
                    new_top_daily_point = models.TopDailyPoint (position=current_tops+1, user=user)
                    new_top_daily_point.save ()
            
    def is_user_live (self, user: models.User):
        """ Return if user is live or not

        Args:
            user (models.User): user object

        Returns:
            bool: True if user is live, False if not
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.access_token}",
            "Client-Id": self.twitch_client_id,
        }

        res = requests.get(f'https://api.twitch.tv/helix/streams?user_id={user.id}', headers=headers)
        
        # Get json data 
        json_data = res.json()
        
        # valdiate if user is live
        is_live = False
        if json_data.get("data"):
            is_live = True
            
        return is_live