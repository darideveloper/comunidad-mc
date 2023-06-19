import json
from django.utils import timezone
from botviews import models
from django.test import TestCase
from django.contrib.auth.models import User as UserAuth

class TestViews (TestCase):

    def setUp(self):

        self.user_name = "test_user"
        self.user_password = "test_password"

        # Test data
        self.token_value = "test_token_value"

        self.endpoint_proxy = f"/botviews/proxy/"
        self.endpoint_users = f"/botviews/users/"
        self.endpoint_update_cookies = f"/botviews/update-cookies" # add username

        self.user = models.User.objects.create(
            name=self.user_name,
            password=self.user_password,
            cookies=[{"test": "test"}],
            is_active=True,
        )

        self.token = models.Token.objects.create(
            name="test_token",
            value="test_token_value",
            is_active=True,
        )
        
        self.proxy = models.Proxy.objects.create(
            host="test_host",
            port=8080,
        )
        
    def test_proxy (self):
        """ Test to get a proxy with endpoint
        """
        
        response = self.client.get(f"{self.endpoint_proxy}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "proxy": {
                "host": self.proxy.host,
                "port": self.proxy.port,
             }
        })
        
    def test_no_proxy (self):
        """ Test to get a proxy with endpoint, where there is no proxies in database
        """
        
        # Delete current proxy
        self.proxy.delete()
        
        response = self.client.get(f"{self.endpoint_proxy}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "proxy": {
                "host": "",
                "port": "",
             }
        })

       
    def test_get_users (self):
        """ Test getting users with endpoint
        """
        
        response = self.client.get(f"{self.endpoint_users}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "users": [
                 {
                    "username": self.user_name,
                    "password": self.user_password,
                 }
             ]
        })
        
    def test_update_cookies_invalid_user (self):
        """ Test try to update user who no exist
        """
        
        response = self.client.post(
            f"{self.endpoint_update_cookies}/this-user-not-exist/?token={self.token_value}",
            json.dumps({"cookies": {"sample": "sample"}}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found"
        })
        
    def test_update_cookies_invalid_data (self):
        """ Test update cookies of user
        """    
        
        response = self.client.post(
            f"{self.endpoint_update_cookies}/{self.user_name}/?token={self.token_value}",
            json.dumps({"sample": "data"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "Cookies not found"    
        })
    
    def test_update_cookies (self):
        """ Test update cookies of user
        """    
        
        response = self.client.post(
            f"{self.endpoint_update_cookies}/{self.user_name}/?token={self.token_value}",
            json.dumps({"cookies": {"sample": "sample"}}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "ok",
            "message": "Cookies updated" 
        })
