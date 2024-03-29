import json
from . import models
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User as UserAuth, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django import forms

class TestModels (TestCase):

    def setUp(self):
        
        # Test data
        self.user_name = "test_user"
        self.user_cookies = [{"test": "test"}]
        self.user_is_active = True
        self.user_password = "test_password"

        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_datetime = timezone.localtime(timezone.now())
        self.donation_amount = 10
        self.donation_message = "hello"

        self.token_name = "test_token"
        self.token_value = "test_token_value"

        # Create test instances
        self.user_auth = UserAuth.objects.create_user(
            email="sample@gmail.com",
            username="sample auth",
            password="sample",
            is_staff=True,
            is_superuser=True
        )

    def test_user(self):
        """ Create and test bot/user
        """

        user = models.User.objects.create(
            name=self.user_name,
            password=self.user_password,
            cookies=self.user_cookies,
            is_active=self.user_is_active,
            user_auth=self.user_auth,
        )

        self.assertEqual(user.name, self.user_name)
        self.assertEqual(user.password, self.user_password)
        self.assertEqual(user.cookies, self.user_cookies)
        self.assertEqual(user.is_active, self.user_is_active)
        self.assertEqual(user.user_auth, self.user_auth)
        self.assertEqual(user.__str__(), "test_user")

    def test_donation(self):
        """ Create and test donation
        """

        user = models.User.objects.create(
            name=self.user_name,
            cookies=self.user_cookies,
            is_active=self.user_is_active,
            user_auth=self.user_auth,
        )

        donation = models.Donation.objects.create(
            user=user,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        self.assertEqual(donation.user, user)
        self.assertEqual(donation.stream_chat_link,
                         self.donation_stream_chat_link)
        self.assertEqual(donation.datetime, self.donation_datetime)
        self.assertEqual(donation.amount, self.donation_amount)
        self.assertEqual(donation.message, self.donation_message)
        self.assertEqual(donation.__str__(),
                         "test_user - 10 bits (sample auth)")

    def test_token(self):
        """ Create and test token
        """

        token = models.Token.objects.create(
            name=self.token_name,
            value=self.token_value,
            is_active=True,
        )

        self.assertEqual(token.name, self.token_name)
        self.assertEqual(token.value, self.token_value)
        self.assertEqual(token.is_active, True)

    def test_proxy (self):
        """ Create and test proxy
        """
        
        proxy = models.Proxy.objects.create(
            host="test_host",
            port=8080,
        )
        
        self.assertEqual (proxy.host, "test_host")
        self.assertEqual (proxy.port, 8080)
        self.assertEqual (proxy.__str__(), "test_host:8080")

class TestViews (TestCase):

    def setUp(self):

        self.user_name = "test_user"
        self.user_password = "test_password"

        # Test data
        self.token_value = "test_token_value"

        self.endpoint_get_donations = f"/botcheers/donations/"
        self.endpoint_disable_user = f"/botcheers/disable-user" # add username
        self.endpoint_update_donation = f"/botcheers/update-donation" # add donation id
        self.endpoint_proxy = f"/botcheers/proxy/"
        self.endpoint_users = f"/botcheers/users/"
        self.endpoint_update_cookies = f"/botcheers/update-cookies" # add username

        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_datetime = timezone.localtime(timezone.now())
        self.donation_amount = 10
        self.donation_message = "hello"

        # Create test instances
        self.user_auth = UserAuth.objects.create_user(
            email="sample@gmail.com",
            username="sample auth",
            password="sample",
            is_staff=True,
            is_superuser=True
        )

        self.user = models.User.objects.create(
            name=self.user_name,
            password=self.user_password,
            cookies=[{"test": "test"}],
            is_active=True,
            user_auth=self.user_auth,
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

    def test_get_donations_invalid_token(self):
        """ Test donations using an invalid token
        """

        response = self.client.get(f"{self.endpoint_get_donations}?token=invalid_token")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test_get_donations_result(self):
        """ Test donations who return data
        """

        # Create donation in the current time
        donation = models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Test response
        response = self.client.get(f"{self.endpoint_get_donations}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "donations": [
                {
                    "id": donation.id,
                    "user": self.user.name,
                    "admin": self.user_auth.username,
                    "stream_chat_link": self.donation_stream_chat_link,
                    "time": self.donation_datetime.strftime("%H:%M:%S.%f")[:12],
                    "amount": self.donation_amount,
                    "message": self.donation_message,
                    "cookies": [{"test": "test"}]
                }
            ]
        })

    def test_get_donations_wrong_time(self):
        """ Test donations who return blank data, because the donations have other time
        """

        # Create donation the next hour
        models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime + timezone.timedelta(hours=1),
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Test response
        response = self.client.get(f"{self.endpoint_get_donations}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "donations": []
        })
        
    def test_get_donations_wrong_date(self):
        """ Test donations who return blank data, because the donations have other date
        """

        # Create donation the next hour
        models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime + timezone.timedelta(days=-1),
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Test response
        response = self.client.get(f"{self.endpoint_get_donations}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
             "donations": []
        })

    def test_disable_user(self):
        """ Test to disable specific user (by name), with endpoint
        """
        
        username = self.user_name

        # Validate response
        response = self.client.get(
            f"{self.endpoint_disable_user}/{username}/?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"User disabled")

        # Validate models
        user = models.User.objects.get(name=username)
        self.assertEqual(user.is_active, False)

    def test_disable_user_error(self):
        """ Test to catch error while disable specific user (by name), with endpoint
        """
        
        username = "invalid_user"

        # Validate response
        response = self.client.get(
            f"{self.endpoint_disable_user}/{username}/?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"User not found")

        # Validate models
        user = models.User.objects.filter(name=username)
        self.assertEqual(user.count(), 0)
    
    def test_update_donation (self):
        """ Test to set to done specific donation (by id), with endpoint
        """
        
        # Create donation
        donation = models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Validate response
        response = self.client.get(
            f"{self.endpoint_update_donation}/{donation.id}/?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Donation updated")

        # Validate models
        donation = models.Donation.objects.filter(id=donation.id)[0]
        self.assertEqual(donation.done, True)

    def test_update_donation_error (self):
        """ Test to catch error while set to done specific donation (by id), with endpoint
        """
        
        donation_id = 999
        
        # Validate response without donation in models
        response = self.client.get(
            f"{self.endpoint_update_donation}/{donation_id}/?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Donation not found")

        # Validate models
        donation = models.Donation.objects.filter(id=donation_id)
        self.assertEqual(donation.count(), 0)
        
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
                    "is_active": True,
                }
            ]
        })
        
    def test_get_users_inactive (self):
        """ Test getting users with endpoint
        """
        
        user = models.User.objects.filter(name=self.user_name)[0]
        user.is_active = False
        user.save ()
        
        response = self.client.get(f"{self.endpoint_users}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "users": [
                {
                    "username": self.user_name,
                    "password": self.user_password,
                    "is_active": False,
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
        
class TestAdmin (TestCase):

    def setUp(self):

        # Test endpoints
        self.endpoint_admin = "/admin"
        self.endpoint_admin_login = f"{self.endpoint_admin}/login/"
        self.endpoint_app = f"{self.endpoint_admin}/botcheers"
        self.endpoint_admin_donation_list = f"{self.endpoint_app}/donation/"
        self.endpoint_admin_donation_add = f"{self.endpoint_app}/donation/add/"
        self.endpoint_admin_user_list = f"{self.endpoint_app}/user/"
        self.endpoint_admin_user_add = f"{self.endpoint_app}/user/add/"

        # Create admin instances

        # Create admin users
        self.user_auth_email = "sample@gmail.com"
        self.user_auth_username = "sample auth"
        self.user_auth_username_pro = "sample auth pro"
        self.user_auth_password = "sample pass"

        self.user_auth_regular = UserAuth.objects.create_user(
            email=self.user_auth_email,
            username=self.user_auth_username,
            password=self.user_auth_password,
            is_staff=True,
        )

        self.user_auth_pro = UserAuth.objects.create_user(
            email=self.user_auth_email,
            username=self.user_auth_username_pro,
            password=self.user_auth_password,
            is_staff=True,
        )

        # Create admin groups
        self.group_bot_cheers_manager = Group.objects.create(
            name="bot cheers manager regular"
        )

        self.group_bot_cheers_manager_pro = Group.objects.create(
            name="bot cheers manager pro"
        )

        # Set permissions to groups
        content_type_user = ContentType.objects.get_for_model(models.User)
        content_type_donations = ContentType.objects.get_for_model(
            models.Donation)

        permissions = []
        permissions += Permission.objects.filter(
            content_type=content_type_user)
        permissions += Permission.objects.filter(
            content_type=content_type_donations)

        for permision in permissions:
            self.group_bot_cheers_manager.permissions.add(permision)
            self.group_bot_cheers_manager_pro.permissions.add(permision)

        # Add groups to users
        self.user_auth_regular.groups.add(self.group_bot_cheers_manager)
        self.user_auth_pro.groups.add(self.group_bot_cheers_manager_pro)

        # Create cheerbot instances

        # Create cheerbot users
        self.user_regular = models.User.objects.create(
            name="test user",
            cookies=[{"test": "test"}],
            is_active=True,
            user_auth=self.user_auth_regular,
        )

        self.user_pro = models.User.objects.create(
            name="test user pro",
            cookies=[{"test": "test"}],
            is_active=True,
            user_auth=self.user_auth_pro,
        )

        # Create cheerbot donations
        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_datetime = timezone.localtime(timezone.now())
        self.donation_amount = 10

        self.donation_regular = models.Donation.objects.create(
            user=self.user_regular,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime,
            amount=self.donation_amount,
            message="donation regular user",
        )

        self.donation_pro = models.Donation.objects.create(
            user=self.user_pro,
            stream_chat_link=self.donation_stream_chat_link,
            datetime=self.donation_datetime + timezone.timedelta(hours=1),
            amount=self.donation_amount,
            message="donation pro user",
        )

        # Create cheerbot tokens
        self.token = models.Token.objects.create(
            name="test_token",
            value="test_token_value",
            is_active=True,
        )

    def login(self, user: str, password: str):
        """ Login to admin with user and password

        Args:
            user (str): username to login
            password (str): password of the user
        """

        # Login in admin with user and password
        response = self.client.post(self.endpoint_admin_login, {
            "username": user,
            "password": password
        }, follow=True)

        # Test redirect after login
        self.assertEqual(response.status_code, 200)

    def test_admin_regular(self):
        """ Test admin home page to regular user
        """

        # Login
        self.login(self.user_auth_username, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin, follow=True)
        self.assertEqual(response.status_code, 200)

        # Validate available tables of response: it should show botcheers tables
        self.assertContains(response, "Botcheers</a>")
        self.assertContains(response, "Bots</a>")
        self.assertContains(response, "Donaciones</a>")

    def test_admin_pro(self):
        """ Test admin home page to pro user
        """

        # Login
        self.login(self.user_auth_username_pro, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin, follow=True)
        self.assertEqual(response.status_code, 200)

        # Validate available tables of response: it should show botcheers tables
        self.assertContains(response, "Botcheers</a>")
        self.assertContains(response, "Bots</a>")
        self.assertContains(response, "Donaciones</a>")

    def test_donation_list_regular(self):
        """ Tets donation list page to regular user
        """

        # Login
        self.login(self.user_auth_username, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_donation_list)
        self.assertEqual(response.status_code, 200)

        # Validate number of rows of response: it should show only current amdin donations
        queryset = response.context["cl"].queryset
        self.assertEqual(queryset.count(), 1)

    def test_donation_list_pro(self):
        """ Tets donation list page to pro user
        """

        # Login
        self.login(self.user_auth_username_pro, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_donation_list)
        self.assertEqual(response.status_code, 200)

        # Validate number of rows of response: it should show all user donations
        queryset = response.context["cl"].queryset
        self.assertEqual(queryset.count(), 2)

    def test_donation_add_regular(self):
        """ Tets add donation page to regular user
        """

        # Login
        self.login(self.user_auth_username, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_donation_add)
        self.assertEqual(response.status_code, 200)

        # Validate rows of response: user options should be all users
        form = response.context['adminform'].form
        queryset = form.fields["user"].queryset
        self.assertEqual(queryset.count(), 1)

    def test_donation_add_pro(self):
        """ Tets add donation page to pro user
        """

        # Login
        self.login(self.user_auth_username_pro, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_donation_add)
        self.assertEqual(response.status_code, 200)

        # Validate rows of response: user options should be all users
        form = response.context['adminform'].form
        queryset = form.fields["user"].queryset
        self.assertEqual(queryset.count(), 2)

    def test_user_list_regular(self):
        """ Tets user list page to regular user
        """

        # Login
        self.login(self.user_auth_username, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_user_list)
        self.assertEqual(response.status_code, 200)

        # Validate number of rows of response: it should show only current amdin donations
        queryset = response.context["cl"].queryset
        self.assertEqual(queryset.count(), 1)

    def test_user_list_pro(self):
        """ Tets user list page to pro user
        """

        # Login
        self.login(self.user_auth_username_pro, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_user_list)
        self.assertEqual(response.status_code, 200)

        # Validate number of rows of response: it should show all user donations
        queryset = response.context["cl"].queryset
        self.assertEqual(queryset.count(), 2)

    def test_user_add_regular(self):
        """ Tets add user page to regular user
        """

        # Login
        self.login(self.user_auth_username, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_user_add)
        self.assertEqual(response.status_code, 200)

        # Validate rows of response: user options should be all users
        form = response.context['adminform'].form
        user_auth = form.fields["user_auth"]
        user_auth_widget = user_auth.widget
        self.assertIsInstance(user_auth_widget, forms.HiddenInput)
        self.assertEqual(user_auth.initial, self.user_auth_regular.id)
        self.assertEqual(user_auth.queryset.count(), 2)

    def test_user_add_pro(self):
        """ Tets add user page to pro user
        """

        # Login
        self.login(self.user_auth_username_pro, self.user_auth_password)

        # Validate response
        response = self.client.get(self.endpoint_admin_user_add)
        self.assertEqual(response.status_code, 200)

        # Validate rows of response: user options should be all users
        form = response.context['adminform'].form
        user_auth = form.fields["user_auth"]
        user_auth_widget = user_auth.widget
        self.assertNotIsInstance(user_auth_widget, forms.HiddenInput)
        self.assertNotEqual(user_auth.initial, self.user_auth_regular.id)
        self.assertEqual(user_auth.queryset.count(), 2)