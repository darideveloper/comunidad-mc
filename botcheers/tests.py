from . import models
from django.test import TestCase
from django.contrib.auth.models import User as UserAuth

class TestModels (TestCase):
    
    def setUp (self):
        
        # Create a user auth
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
            name = "test_user",
            cookies = {"test": "test"},
            is_active = True,
            user_auth = self.user_auth,
        )
        
        self.assertEqual (user.name, "test_user")
        self.assertEqual (user.cookies, {"test": "test"})
        self.assertEqual (user.is_active, True)
        self.assertEqual (user.user_auth, self.user_auth)
        self.assertEqual (user.__str__(), "test_user")
    
    def test_donation (self):
        """ Create and test donation
        """
        
        user = models.User.objects.create (
            name = "test_user",
            cookies = {"test": "test"},
            is_active = True,
            user_auth = self.user_auth,
        )
        
        donation = models.Donation.objects.create (
            user = user,
            stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout=",
            hour = 1,
            minute = 1,
            amount = 10,
            message = "hello",
        )
                
        self.assertEqual (donation.user, user)
        self.assertEqual (donation.stream_chat_link, "https://www.twitch.tv/popout/auronplay/chat?popout=")
        self.assertEqual (donation.hour, 1)
        self.assertEqual (donation.minute, 1)
        self.assertEqual (donation.amount, 10)
        self.assertEqual (donation.message, "hello")
        self.assertEqual (donation.__str__(), "test_user - 10 bits (sample_auth)")
        
    
    def test_token (self):
        """ Create and test token
        """
        
        token = models.Token.objects.create (
            name = "test_token",
            value = "test_value",
            is_active = True,
        )
        
        self.assertEqual (token.name, "test_token")
        self.assertEqual (token.value, "test_value")
        self.assertEqual (token.is_active, True)
        
# class TestViews (TestCase):
    
#     def setUp (self):
        
#         # Create a user auth
#         self.user_auth = UserAuth.objects.create_user (
#             email="sample@gmail.com",
#             username="sample_auth",
#             password="sample",
#             is_staff=True,
#             is_superuser=True
#         )
        
#         self.user = models.User.objects.create (
#             name = "test_user",
#             cookies = {"test": "test"},
#             is_active = True,
#             user_auth = self.user_auth,
#         )
        
#         self.donation = models.Donation.objects.create (
#             user = self.user,
#             stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout=",
#             hour = 1,
#             minute = 1,
#             amount = 10,
#             message = "hello",
#         )
        
#     def test_get_donations_result (self):
#         """ Test donations who return data
#         """
#         self.donation = models.Donation.objects.create (
#             user = self.user,
#             stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout=",
#             hour = 1,
#             minute = 1,
#             amount = 10,
#             message = "hello",
#         )
    
#     def test_get_donations_balnk (self): 
#         """ Test donations who return blank data
#         """
#         pass
    
    
        
    