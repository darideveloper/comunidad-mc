from . import models
from django.test import TestCase
from django.contrib.auth.models import User as UserAuth, Group
from django.utils import timezone
from django.urls import reverse

class TestModels (TestCase):
    
    def setUp (self):
        
        
        # Test data
        self.user_name = "test_user"
        self.user_cookies = [{"test": "test"}]
        self.user_is_active = True
        
        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_hour = 1
        self.donation_minute = 1
        self.donation_amount = 10
        self.donation_message = "hello"
        
        self.token_name = "test_token"
        self.token_value = "test_token_value"
        
        # Create test instances
        self.user_auth = UserAuth.objects.create_user (
            email="sample@gmail.com",
            username="sample_auth",
            password="sample",
            is_staff=True,
            is_superuser=True
        )
        
    def test_user (self):
        """ Create and test bot/user
        """
        
        user = models.User.objects.create (
            name = self.user_name,
            cookies = self.user_cookies,
            is_active = self.user_is_active,
            user_auth = self.user_auth,
        )
        
        self.assertEqual (user.name, self.user_name)
        self.assertEqual (user.cookies, self.user_cookies)
        self.assertEqual (user.is_active, self.user_is_active)
        self.assertEqual (user.user_auth, self.user_auth)
        self.assertEqual (user.__str__(), "test_user")
    
    def test_donation (self):
        """ Create and test donation
        """
        
        user = models.User.objects.create (
            name = self.user_name,
            cookies = self.user_cookies,
            is_active = self.user_is_active,
            user_auth = self.user_auth,
        )
        
        donation = models.Donation.objects.create (
            user = user,
            stream_chat_link = self.donation_stream_chat_link,
            hour = self.donation_hour,
            minute = self.donation_minute,
            amount = self.donation_amount,
            message = self.donation_message,
        )
                
        self.assertEqual (donation.user, user)
        self.assertEqual (donation.stream_chat_link, self.donation_stream_chat_link)
        self.assertEqual (donation.hour, self.donation_hour)
        self.assertEqual (donation.minute, self.donation_minute)
        self.assertEqual (donation.amount, self.donation_amount)
        self.assertEqual (donation.message, self.donation_message)
        self.assertEqual (donation.__str__(), "test_user - 10 bits (sample_auth)")
        
    
    def test_token (self):
        """ Create and test token
        """
        
        token = models.Token.objects.create (
            name = self.token_name,
            value = self.token_value,
            is_active = True,
        )
        
        self.assertEqual (token.name, self.token_name)
        self.assertEqual (token.value, self.token_value)
        self.assertEqual (token.is_active, True)
        
class TestViews (TestCase):
    
    def setUp (self):
        
        # Test data
        self.token_value = "test_token_value"
        
        self.endpoint_get_dinations = f"/botcheers/donations/"
    
        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_hour = timezone.localtime(timezone.now()).hour
        self.donation_minute = 1
        self.donation_amount = 10
        self.donation_message = "hello"
        
        # Create test instances
        self.user_auth = UserAuth.objects.create_user (
            email="sample@gmail.com",
            username="sample_auth",
            password="sample",
            is_staff=True,
            is_superuser=True
        )
        
        self.user = models.User.objects.create (
            name = "test_user",
            cookies = [{"test": "test"}],
            is_active = True,
            user_auth = self.user_auth,
        )
        
        self.token = models.Token.objects.create (
            name = "test_token",
            value = "test_token_value",
            is_active = True,
        )
        
    def test_get_dinations_invalid_token (self):
        """ Test donations using an invalid token
        """
        
        response = self.client.get (f"{self.endpoint_get_dinations}?token=invalid_token")
        self.assertEqual (response.status_code, 400)
        self.assertEqual (response.content, b"Invalid token")
    
    def test_get_donations_result (self):
        """ Test donations who return data
        """
        
        # Create donation in the current hour
        models.Donation.objects.create (
            user = self.user,
            stream_chat_link = self.donation_stream_chat_link,
            hour = self.donation_hour,
            minute = self.donation_minute,
            amount = self.donation_amount,
            message = self.donation_message,
        )
        
        # Test response
        response = self.client.get (f"{self.endpoint_get_dinations}?token={self.token_value}")
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.json(), [
            {
                "user": self.user.name,
                "admin": self.user_auth.username,
                "stream_chat_link": self.donation_stream_chat_link,
                "hour": self.donation_hour,
                "minute": self.donation_minute,
                "amount": self.donation_amount,
                "message": self.donation_message,
                "cookies": [{"test": "test"}]
            }
        ])
    
    def test_get_donations_balnk (self): 
        """ Test donations who return blank data
        """
        
        # Create donation the next hour
        models.Donation.objects.create (
            user = self.user,
            stream_chat_link = self.donation_stream_chat_link,
            hour = self.donation_hour + 1,
            minute = self.donation_minute,
            amount = self.donation_amount,
            message = self.donation_message,
        )
        
        # Test response
        response = self.client.get (f"{self.endpoint_get_dinations}?token={self.token_value}")
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.json(), [])
    
# class TestAdmin (TestCase):
    
#     def setUp (self):
    
#         # Create admin instances
#         self.user_auth = UserAuth.objects.create_user (
#             email="sample@gmail.com",
#             username="sample_auth",
#             password="sample",
#             is_staff=True,
#             is_superuser=True
#         )
    
#         self.group_bot_cheers_manager = Group.objects.create (
#             name = "Bot Cheers Manager"
#         )
        
#         # Create cheerbot instances
#         self.user = models.User.objects.create (
#             name = "test_user",
#             cookies = [{"test": "test"}],
#             is_active = True,
#             user_auth = self.user_auth,
#         )
        
#         self.token = models.Token.objects.create (
#             name = "test_token",
#             value = "test_token_value",
#             is_active = True,
#         )
