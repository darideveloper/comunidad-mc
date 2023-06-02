import os
import pytz
import json
import requests
import datetime
from . import models
from .logs import logger
from dotenv import load_dotenv
from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from . import tools


class TwitchApi:

    def __init__(self):
        # Load and get credentials
        load_dotenv()
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
        logger.debug("Getting streams from database for current hour")
        now_datetime = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE))
        start_hour = now_datetime.replace(minute=0, second=0, microsecond=0)
        end_hour = now_datetime.replace(
            minute=59, second=59, microsecond=999999)

        # Get current streams
        current_streams = models.Stream.objects.filter(
            datetime__range=[start_hour, end_hour]).all().order_by('user__user_name')

        if not current_streams:
            logger.info("No streams found")
            return []

        return current_streams

    # def get_current_streams_node(self):
    #     """ Get the current live streams from databse

    #     Returns:
    #         models.Stream.objects: Streams instances
    #     """

    #     # Get date ranges
    #     logger.debug ("Getting streams from database for current hour")
    #     now_datetime = timezone.now().astimezone(pytz.timezone (settings.TIME_ZONE))
    #     start_hour = now_datetime.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    #     end_hour = now_datetime.replace(minute=59, second=59, microsecond=999999) + datetime.timedelta(hours=1)

    #     # Get current streams
    #     current_streams = models.Stream.objects.filter(
    #         datetime__range=[start_hour, end_hour]).all().order_by('user__user_name')

    #     if not current_streams:
    #         logger.info("No streams found")
    #         return []

    #     return current_streams

    def submit_streams_node(self):
        """ Submit streams to node.js api for start reading comments

        Args:
            self.node_api (str): url of node.js api

        Returns:
            bool: True if node.js api is working, False if not
        """

        node_error = False
        current_streams = self.get_current_streams()
        logger.info(f"Sending streams to node.js api: {len(current_streams)}")
        # debug streams found
        logger.info(
            f"Streams found: {','.join(list(map(lambda stream: stream.user.user_name, current_streams)))}")

        # Detect unique user of the streams
        users = list(
            set(map(lambda current_stream: current_stream.user, current_streams)))
        users_names = list(map(lambda user: user.user_name, users))

        # Refresh tokens
        logger.info(f"Refreshing tokens for users: {','.join(users_names)}")
        for user in users:
            token_updated = self.update_token(user)
            if not token_updated:
                logger.error(f"Error updating token for user: {user}")

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
            "chat:read",
            "moderator:read:chatters",
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
    
    def __get_watch_users__ (self, streamer: models.User):
        """ get users who are currently watching a stream

        Args:
            stream (models.Stream): stream to get users
        """
        
         # Loop for get data and update token
        while True:

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
            if "error" in json_data and "message" in json_data:
                
                # Debug scope errors
                if "Missing scope" in json_data["message"]:
                    logger.error (f"Unauthorized to get chat users for user {streamer}: {json_data}")
                    break
                
                # Show error and try again
                logger.error(
                    f"Token expired for {streamer}. Details: {json_data}.)")
                self.update_token(streamer)
                continue
            else:
                break

        # Get users in chat
        users_active = list(
            map(lambda user: user["user_id"], json_data.get("data", [])))
        
        return users_active

    def check_users_in_chat(self):
        """ Get list of users in chat of the current streams and save in databse """

        # Get current streams and loop
        current_streams = self.get_current_streams()
        if not current_streams:
            return None

        for stream in current_streams:
            
            # Get current stream
            streamer = stream.user
            
            # Get watch users of the current streams
            watch_users = self.__get_watch_users__(streamer)

            # Filter only user who exist in database
            valid_users = models.User.objects.filter(id__in=watch_users)
            if len(valid_users) == 1:
                logger.info(f"No users in stream: {stream}")

            # Update first_stream_done from user
            referred_user_from = streamer.referred_user_from
            first_stream_done = streamer.first_stream_done
            if valid_users and not first_stream_done and referred_user_from:

                logger.info(
                    f"First stream detected from referred user {streamer}")

                # Update streamer data
                streamer.first_stream_done = True
                streamer.save()

                # Add 10 general points to referred_user_from
                info_point = models.InfoPoint.objects.get(info="primer stream de referido")
                models.GeneralPoint.objects.create(
                    user=referred_user_from,
                    amount=10,
                    info=info_point,
                ).save ()

                # Add bits to streamer
                models.Bit.objects.create(
                    user=referred_user_from, 
                    amount=100, 
                    details=f"Referido {streamer}"
                ).save ()
                
                logger.info (f"Reward added to user {referred_user_from}")
                                
            # Save in each watch in database
            for user in valid_users:

                # Skip if user is the streamer
                if user.id == streamer.id:
                    continue
                
                # Validate if user already have a general point in the stream
                general_point_found = models.GeneralPoint.objects.filter(stream=stream, user=user, amount__gte=1).exists()
                if general_point_found:
                    logger.info (f"User {user} already have a general point in stream {stream}. Check skipped.")
                    continue
                
                # Save check in database
                new_check = models.WhatchCheck(stream=stream, user=user)
                new_check.save()
                logger.info(f"Check saved. User: {user}, Stream: {stream}")

                # Add cero point (initial default point) to user
                self.add_cero_point(user, stream)

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

    def update_token(self, user: models.User):
        """ Update user token and save in database

        Args:
            user (models.User): user instance

        Returns: 
            bool: True if token updated, False if error
        """

        # Get new access token using refresh token
        new_access_token = self.get_new_user_token(user.refresh_token)
        if not new_access_token:
            logger.error(f"Error generating new token for user: {user}")
            return False

        # Update user token
        user.access_token = new_access_token
        user.save()
        logger.info(f"User token updated: {user}")
        return True

    def add_point(self, user: models.User, stream: models.Stream = None, force: bool = False):
        """ Add point to user after watch stream and comment in chat

        Args:
            user (models.User): user instance
            stream (models.Stream, optional): stream instance. Defaults to None.           
        """

        # Get live streams where no stream spificied
        current_streams = [stream]
        if not stream:
            current_streams = self.get_current_streams()

        # Loop for ech stream
        for stream in current_streams:

            # Get users whatch checks
            user_checks = models.WhatchCheck.objects.filter(
                user=user, stream=stream, status=1)

            # Get users comments
            user_comments = models.Comment.objects.filter(
                user=user, stream=stream, status=1)

            # Validate min number of checks and comments
            if (len(user_checks) >= self.min_checks and len(user_comments) >= self.min_comments) or force:

                # Get streamer
                streamer = stream.user
                amount = 1

                # Subtract point to streamer (except rankings: admin and free streams)
                admin_type = tools.get_admin_type(user=streamer)
                if not admin_type and not stream.is_free:
                    tools.set_negative_point(streamer, 1, "viwer asistió a stream", stream)

                # Set tripple point if stream is vip or if triple time
                is_triple_time = tools.is_triple_time()
                if stream.is_vip or is_triple_time:
                    # Add 2 points to user
                    info = models.InfoPoint.objects.get(info="ver stream (puntos extra)")
                    models.GeneralPoint (user=user, stream=stream, amount=2, info=info).save()

                logger.info(f"Added {amount} general points to user: {user}")

                # Get and update general point
                info = models.InfoPoint.objects.get(info="ver stream")
                new_general_point = models.GeneralPoint.objects.filter (user=user, stream=stream, amount=0)
                if not new_general_point:
                    logger.error (f"Error adding general point to user {user} in stream {stream} (0 general point, not found)")
                    continue
                new_general_point = new_general_point[0]
                new_general_point.amount = amount
                new_general_point.info = info
                new_general_point.save()
                
                # Validate if user already have a daily point in this hour
                start_time = timezone.now().replace(minute=0, second=0) - datetime.timedelta(minutes=1)
                end_time = timezone.now().replace(minute=59, second=59)
                daily_points_hour = models.DailyPoint.objects.filter(
                    general_point__user=user, general_point__stream__datetime__range=[start_time, end_time])
                
                if daily_points_hour:
                    logger.info (f"User {user} already have a daily point in this hour: {daily_points_hour}")
                else:

                    # Validate if the user have less than the max number of daily points
                    daily_points = models.DailyPoint.objects.filter(
                        general_point__user=user)
                    current_daily_points = daily_points.aggregate(Sum('general_point__amount'))[
                        'general_point__amount__sum']
                    if not current_daily_points:
                        current_daily_points = 0

                    if current_daily_points < self.max_daily_points:

                        # Validate if already exists daily and weekly point
                        current_daily_point = models.DailyPoint.objects.filter(
                            general_point=new_general_point).count()

                        # Save daily point
                        if current_daily_point == 0:
                            new_daily_point = models.DailyPoint(
                                general_point=new_general_point)
                            new_daily_point.save()

                        logger.info(f"Added daily to user: {user}")

                        # Check if there are less than 10 users in the Ranking of daily points and if user already have 10 points
                        current_tops = models.TopDailyPoint.objects.all().count()
                        current_points = current_daily_points + 1
                        if current_tops < 10 and current_points == 10:

                            # Add user to Ranking of daily points if there isnt in table
                            user_in_top = models.TopDailyPoint.objects.filter(
                                user=user).count()
                            if user_in_top == 0:
                                logger.info(
                                    f"User {user} already have 10 points. Added to Ranking of daily points")
                                new_top_daily_point = models.TopDailyPoint(
                                    position=current_tops+1, user=user)
                                new_top_daily_point.save()

                # Set done status to comments and checks
                done_status = models.Status.objects.get(id=2)
                for check in user_checks:
                    check.status = done_status
                    check.save()

                for comment in user_comments:
                    comment.status = done_status
                    comment.save()

    def is_user_live(self, user: models.User):
        """ Return if user is live or not

        Args:
            user (models.User): user object

        Returns:
            bool: True if user is live, False if not
        """
        
        is_live = False
        while True:
            
            print (f"Checking if user {user} is live")
                    
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {user.access_token}",
                "Client-Id": self.twitch_client_id,
            }

            res = requests.get(
                f'https://api.twitch.tv/helix/streams?user_id={user.id}', headers=headers)

            # Get json data
            json_data = res.json()
            
            if res.status_code != 200:
                print (f"\tUpdate token for user {user}")
                self.update_token(user)
                continue
                
            # valdiate if user is live
            if json_data.get("data"):
                is_live = True
           
            break
            
        print (f"\tUser {user} is live: {is_live}")

        return is_live

    def update_twitch_data(self, user: models.User):
        """ Update twitch user name, profile image and id

        Args:
            user (models.User): user object
        """
        
        print (user)

        # Refresh token
        token_updated = self.update_token(user)

        if not token_updated:
            return False

        token = user.access_token

        # Get user data
        user_id, user_email, user_picture, user_name = self.get_user_info(token)
        print (user_id, user_email, user_picture, user_name)

        # Save new data
        user.id = user_id
        user.email = user_email
        user.picture = user_picture
        user.user_name = user_name
        user.save()

        return True

    def add_cero_point(self, user: models.User, stream: models.Stream):
        """ Set a point register with amount in 0 when is the first check or comment of the user in the stream """

        # Validate if the user already have a point in the stream
        general_points = models.GeneralPoint.objects.filter(
            user=user, stream=stream)
        if general_points.count() == 0:

            # Save general point
            info = models.InfoPoint.objects.get(
                info="faltó tiempo de visualización o comentarios")
            models.GeneralPoint.objects.create(
                user=user, stream=stream, amount=0, info=info).save()
