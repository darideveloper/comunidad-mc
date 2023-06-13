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

    def __init__(self, logs_prefix:str=""):
        # Load and get credentials
        load_dotenv()
        self.node_api = os.environ.get("NODE_API")
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.twitch_secret = os.getenv("TWITCH_SECRET")
        self.min_comments = int(os.getenv("MIN_COMMENTS"))
        self.min_time_comments = int(os.getenv("MIN_TIME_COMMENTS"))
        self.max_daily_points = int(os.getenv("MAX_DAILY_POINTS"))
        self.wait_minutes_points = int(os.getenv("WAIT_MINUTES_POINTS"))
        
        # Logs
        self.logs_prefix = logs_prefix

    def get_current_streams(self, back_hours:int=0):
        """ Get the current live streams from databse
        
        Args:
            back_hours (int, optional): hours to go back in time. Defaults to 0.

        Returns:
            models.Stream.objects: Streams instances
        """

        # Get date ranges
        logger.debug(f"{self.logs_prefix} Getting streams from database for current hour")
        now_datetime = timezone.now().astimezone(pytz.timezone(settings.TIME_ZONE)) - datetime.timedelta(hours=back_hours)
        start_hour = now_datetime.replace(minute=0, second=0, microsecond=0)
        end_hour = now_datetime.replace(
            minute=59, second=59, microsecond=999999
        )

        # Get current streams
        current_streams = models.Stream.objects.filter(
            datetime__range=[start_hour, end_hour]).all().order_by('user__user_name')

        if not current_streams:
            logger.info(f"{self.logs_prefix} No streams found")
            return []

        return current_streams

    def submit_streams_node(self):
        """ Submit streams to node.js api for start reading comments

        Args:
            self.node_api (str): url of node.js api

        Returns:
            bool: True if node.js api is working, False if not
        """

        node_error = False
        current_streams = self.get_current_streams()
        logger.info(f"{self.logs_prefix} Sending streams to node.js api: {len(current_streams)}")
        # debug streams found
        logger.info(
            f"{self.logs_prefix} Streams found: {','.join(list(map(lambda stream: stream.user.user_name, current_streams)))}"
        )
        
        # Update streamer tokens
        for stream in current_streams:
            self.update_token (stream.user)

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
            logger.info(f"{self.logs_prefix} Sending streams to node.js api")
            res = requests.post(self.node_api, json=streams_data)
            res.raise_for_status()
        except Exception as e:
            logger.error(f"{self.logs_prefix} Error sending streams to node.js api: {e}")
            node_error = True

        return node_error

    def is_node_working(self):
        """ Submit a basic request to node.js api to check if is working

        Args:
            self.node_api (str): url of node.js api

        Returns:
            bool: True if node.js api is working, False if not
        """

        logger.info(f"{self.logs_prefix} Checking if node.js api is working")
        try:
            res = requests.post(self.node_api)
        except Exception as e:
            logger.error(f"{self.logs_prefix} Error checking if node.js api is working: {e}")
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
        
        logger.info (f"{self.logs_prefix} Getting tokens from twitch api")

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

        # Extract variables
        access_token = json_data.get("access_token", "")
        refresh_token = json_data.get("refresh_token", "")
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
            "force_verify": "false",
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
            return []

        # Validate if token is expired and retry
        if "error" in json_data and "message" in json_data:
            
            # Debug scope errors
            if "Missing scope" in json_data["message"]:
                logger.error (f"{self.logs_prefix} Unauthorized to get chat users for user {streamer}: {json_data}")
                return []
            
            # Show error and try again
            logger.error(f"{self.logs_prefix} Token expired for {streamer}. Details: {json_data}.)")
            return []

        # Get users in chat
        users_active = list(
            map(lambda user: user["user_id"], json_data.get("data", []))
        )
        
        return users_active

    # def check_users_in_chat(self):
    #     """ Get list of users in chat of the current streams and save in databse """

    #     # Get current streams and loop
    #     current_streams = self.get_current_streams()
    #     current_streams_ids = list(map(lambda stream: stream.id, current_streams))
    #     print (f"Checking users in chat of streams {current_streams}")
    #     if not current_streams:
    #         return None

    #     for stream in current_streams:
            
    #         # Get current stream
    #         streamer = stream.user
            
    #         # Get watch users of the current streams
    #         watch_users = self.__get_watch_users__(streamer)

    #         # Filter only user who exist in database
    #         valid_users = models.User.objects.filter(id__in=watch_users)
    #         if len(valid_users) == 1:
    #             logger.info(f"No users in stream: {stream}")

    #         # Update first_stream_done from user
    #         referred_user_from = streamer.referred_user_from
    #         first_stream_done = streamer.first_stream_done
    #         if valid_users and not first_stream_done and referred_user_from:

    #             logger.info(
    #                 f"First stream detected from referred user {streamer}")

    #             # Update streamer data
    #             streamer.first_stream_done = True
    #             streamer.save()

    #             # Add 10 general points to referred_user_from
    #             info_point = models.InfoPoint.objects.get(info="primer stream de referido")
    #             general_point = models.GeneralPoint.objects.create(
    #                 user=referred_user_from,
    #                 amount=10,
    #                 info=info_point,
    #             )
                
    #             # Add weekly points to referred_user_from
    #             models.WeeklyPoint.objects.create(
    #                 general_point=general_point,                    
    #             )

    #             # Add bits to streamer
    #             models.Bit.objects.create(
    #                 user=referred_user_from, 
    #                 amount=100, 
    #                 details=f"Referido {streamer}"
    #             )
                
    #             logger.info (f"Reward added to user {referred_user_from}")
                                
    #         # Save in each watch in database
    #         for user in valid_users:

    #             # Skip if user is live
    #             if user.id in current_streams_ids:
    #                 continue
                
    #             # Validate if user already have a general point in the stream
    #             general_point_found = models.GeneralPoint.objects.filter(stream=stream, user=user, amount__gte=1).exists()
    #             if general_point_found:
    #                 logger.info (f"User {user} already have a general point in stream {stream}. Check skipped.")
    #                 continue
                
    #             # Save check in database
    #             new_check = models.WhatchCheck(stream=stream, user=user)
    #             new_check.save()
    #             logger.info(f"Check saved. User: {user}, Stream: {stream}")

    #             # Add cero point (initial default point) to user
    #             self.add_cero_point(user, stream)

    #             # Try to add point to user
    #             self.add_point(user, stream)

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
                f"{self.logs_prefix} Error updating user refresh_token: ({res.status_code}) {refresh_token}")
            return ""

        json_data = res.json()
        access_token = json_data.get("access_token", "")
        if not access_token:
            logger.error(
                f"{self.logs_prefix} Error updating user refresh_token: ({res.status_code}) {refresh_token}")
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
            logger.error(f"{self.logs_prefix} Error generating new token for user: {user}")
            return False

        # Update user token
        user.access_token = new_access_token
        user.save()
        logger.info(f"{self.logs_prefix} User token updated: {user}")
        return True

    def add_point(self, user:models.User, stream:models.Stream, force:bool=False, amount:int=1, info_text:str="ver stream"):
        """ Add point to user after stream

        Args:
            user (models.User): user object
            stream (models.Stream): stream object
            force (bool, optional): Force add point. Defaults to False.
            amount (int, optional): Amount of points. Defaults to 1.
            info_text (str, optional): Details of the point. Defaults to "ver stream".
        """

        # Get streamer
        streamer = stream.user

        # Subtract point to streamer (except rankings: admin and free streams)
        admin_type = tools.get_admin_type(user=streamer)
        if not admin_type and not stream.is_free and not force and amount >= 1:
            tools.set_negative_point(streamer, 1, "viwer asistió a stream", prefix=self.logs_prefix)

        # Set tripple point if stream is vip or if triple time
        is_triple_time = tools.is_triple_time()
        if (stream.is_vip or is_triple_time) and not force:
            # Add 2 points to user
            info = models.InfoPoint.objects.get(info="ver stream (puntos extra)")
            models.GeneralPoint.objects.create( # debug
                user=user,
                stream=stream,
                amount=2,
                info=info,
            )


        # add general point
        info = models.InfoPoint.objects.get(info=info_text)
        general_point = None
        general_point = models.GeneralPoint.objects.create( # debug
            user=user,
            stream=stream,
            amount=amount,
            info=info,
        )
        
        logger.info(f"{self.logs_prefix} Added {amount} general points to user: {user}")
        
        # Validate if user already have a daily point in this hour
        start_time = timezone.now().replace(minute=0, second=0) - datetime.timedelta(minutes=1)
        end_time = timezone.now().replace(minute=59, second=59)
        daily_points_hour = models.DailyPoint.objects.filter(
            general_point__user=user, 
            general_point__stream__datetime__range=[start_time, end_time]
        )
        
        if daily_points_hour and not force:
            id = daily_points_hour.first().general_point.id
            logger.info (
                f"{self.logs_prefix} User {user} already have a daily point in this hour: {id}"
            )
        else:

            # Validate if the user have less than the max number of daily points
            daily_points = models.DailyPoint.objects.filter(
                general_point__user=user
            )
            daily_points_positive = daily_points.filter(
                general_point__amount__gte=1
            )
            current_daily_points = daily_points_positive.aggregate(Sum('general_point__amount'))['general_point__amount__sum']
            if not current_daily_points:
                current_daily_points = 0

            if current_daily_points < self.max_daily_points:

                # Validate if already exists daily and weekly point
                current_daily_point = models.DailyPoint.objects.filter(
                    general_point=general_point
                ).count()

                # Save daily point
                if current_daily_point == 0:
                    models.DailyPoint.objects.create ( # debug
                        general_point=general_point
                    )

                    logger.info(f"{self.logs_prefix} Added daily to user: {user}")

                # Check if there are less than 10 users in the Ranking of daily points and if user already have 10 points
                current_tops = models.TopDailyPoint.objects.all().count()
                current_points = current_daily_points + 1
                if current_tops < 10 and current_points == 10:

                    # Add user to Ranking of daily points if there isnt in table
                    user_in_top = models.TopDailyPoint.objects.filter(
                        user=user
                    ).count()
                    
                    if not user_in_top:
                        models.TopDailyPoint.objects.create( # debug
                            position=current_tops+1, user=user
                        )
                        logger.info(f"{self.logs_prefix} User {user} already have 10 points. Added to Ranking of daily points")

    def is_user_live(self, user: models.User):
        """ Return if user is live or not

        Args:
            user (models.User): user object

        Returns:
            bool: True if user is live, False if not
        """
        
        is_live = False            
        logger.info (f"{self.logs_prefix} Checking if user {user} is live")
                
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.access_token}",
            "Client-Id": self.twitch_client_id,
        }

        res = requests.get(
            f'https://api.twitch.tv/helix/streams?user_id={user.id}', headers=headers)

        # Get json data
        json_data = res.json()
        
        if res.status_code == 200:
            # valdiate if user is live
            if json_data.get("data"):
                is_live = True
        else:
            logger.info (f"{self.logs_prefix} Can't check live. Invalid token for user {user}")
                    
        logger.info (f"{self.logs_prefix} User {user} is live: {is_live}")

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

    def add_cero_point(self, user: models.User, stream:models.Stream, info_text:str):
        """ Set a point register with amount in 0 when is the first check or comment of the user in the stream

        Args:
            user (models.User): user object
            stream (models.Stream): stream object
            info_text (str, optional): details of the point.
        """

        # Save general point
        info = models.InfoPoint.objects.get(
            info=info_text
        )
        models.GeneralPoint.objects.create( # debug
            user=user, stream=stream, amount=0, info=info
        )

    def calculate_points (self):
        """ Count comments in the current streams and set points to users """
        
        current_streams = self.get_current_streams()
        if not current_streams:
            logger.info (f"{self.logs_prefix} No streams found at this hour")
        stream_text = ",".join(list(map(lambda stream: stream.user.user_name, current_streams)))
        logger.info (f"{self.logs_prefix} Calculating points for streams: {stream_text}")
        
        users = models.User.objects.all()    
        
        for stream in current_streams:
            
            for user in users:
                
                
                # Get comments of the user in the stream
                comments = models.Comment.objects.filter(user=user, stream=stream, status=1)
                comments_num = comments.count()
                if not comments:
                    continue
                
                # Validate comment ammount          
                if (comments_num < self.min_comments):
                    # Add cero point
                    logger.info (f"{self.logs_prefix} User {user} have only {comments_num} comments in stream {stream}")
                    self.add_cero_point (user, stream, info_text="faltaron comentarios")
                    continue
                
                # Validate distance between first and last comment  
                first_comment = comments.first()
                last_comment = comments.last()
                time_between = (last_comment.datetime - first_comment.datetime).total_seconds() / 60.0
                if (time_between < self.min_time_comments):
                    
                    # Add cero point
                    logger.info (f"{self.logs_prefix} User {user} have less than {self.min_time_comments} minutes between first and last comment in stream {stream}")
                    self.add_cero_point (user, stream, info_text="faltó tiempo de visualización")
                    continue
                
                # Add point
                self.add_point(user, stream, amount=1, info_text="ver stream")
            
                # Update comments status
                done_status = models.Status.objects.get(name="done")
                for comment in comments:
                    comment.status = done_status
                    comment.save()