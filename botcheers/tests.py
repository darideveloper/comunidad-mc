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

        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_hour = 1
        self.donation_minute = 1
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
            cookies=self.user_cookies,
            is_active=self.user_is_active,
            user_auth=self.user_auth,
        )

        self.assertEqual(user.name, self.user_name)
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
            hour=self.donation_hour,
            minute=self.donation_minute,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        self.assertEqual(donation.user, user)
        self.assertEqual(donation.stream_chat_link,
                         self.donation_stream_chat_link)
        self.assertEqual(donation.hour, self.donation_hour)
        self.assertEqual(donation.minute, self.donation_minute)
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


class TestViews (TestCase):

    def setUp(self):

        self.user_name = "test_user"

        # Test data
        self.token_value = "test_token_value"

        self.endpoint_get_dinations = f"/botcheers/donations/"
        self.endpoint_disable_user = f"/botcheers/disable-user" # add name

        self.donation_stream_chat_link = "https://www.twitch.tv/popout/auronplay/chat?popout="
        self.donation_hour = timezone.localtime(timezone.now()).hour
        self.donation_minute = 1
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
            cookies=[{"test": "test"}],
            is_active=True,
            user_auth=self.user_auth,
        )

        self.token = models.Token.objects.create(
            name="test_token",
            value="test_token_value",
            is_active=True,
        )

    def test_get_dinations_invalid_token(self):
        """ Test donations using an invalid token
        """

        response = self.client.get(
            f"{self.endpoint_get_dinations}?token=invalid_token")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid token")

    def test_get_donations_result(self):
        """ Test donations who return data
        """

        # Create donation in the current hour
        models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            hour=self.donation_hour,
            minute=self.donation_minute,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Test response
        response = self.client.get(
            f"{self.endpoint_get_dinations}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
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

    def test_get_donations_balnk(self):
        """ Test donations who return blank data
        """

        # Create donation the next hour
        models.Donation.objects.create(
            user=self.user,
            stream_chat_link=self.donation_stream_chat_link,
            hour=self.donation_hour + 1,
            minute=self.donation_minute,
            amount=self.donation_amount,
            message=self.donation_message,
        )

        # Test response
        response = self.client.get(
            f"{self.endpoint_get_dinations}?token={self.token_value}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

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
        self.donation_hour = timezone.localtime(timezone.now()).hour
        self.donation_minute = 1
        self.donation_amount = 10

        self.donation_regular = models.Donation.objects.create(
            user=self.user_regular,
            stream_chat_link=self.donation_stream_chat_link,
            hour=self.donation_hour,
            minute=self.donation_minute,
            amount=self.donation_amount,
            message="donation regular user",
        )

        self.donation_pro = models.Donation.objects.create(
            user=self.user_pro,
            stream_chat_link=self.donation_stream_chat_link,
            hour=self.donation_hour + 1,
            minute=self.donation_minute,
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
