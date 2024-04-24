from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import (
    EmailTokenObtainPairView,
    GoogleConnect,
    GoogleLogin,
    LinkedInLogin,
    LinkedInConnect,
    RegisterView,
    TodoViewSet,
    UserViewSet,
    GetWSTokenView,
)


class UrlResolveTests(SimpleTestCase):
    def test_google_login_url_resolves(self):
        """
        Test Google login URL resolves to the correct view.
        """
        url = reverse("api:google_login")
        self.assertEqual(resolve(url).func.view_class, GoogleLogin)

    def test_linkedin_login_url_resolves(self):
        """
        Test LinkedIn login URL resolves to the correct view.
        """
        url = reverse("api:linkedin_login")
        self.assertEqual(resolve(url).func.view_class, LinkedInLogin)

    def test_google_connect_url_resolves(self):
        """
        Test Google connect URL resolves to the correct view.
        """
        url = reverse("api:google_connect")
        self.assertEqual(resolve(url).func.view_class, GoogleConnect)

    def test_linkedin_connect_url_resolves(self):
        """
        Test LinkedIn connect URL resolves to the correct view.
        """
        url = reverse("api:linkedin_connect")
        self.assertEqual(resolve(url).func.view_class, LinkedInConnect)

    def test_token_obtain_pair_url_resolves(self):
        """
        Test token obtain pair URL resolves to the correct view.
        """
        url = reverse("api:token_obtain_pair")
        self.assertEqual(resolve(url).func.view_class, EmailTokenObtainPairView)

    def test_token_refresh_url_resolves(self):
        """
        Test token refresh URL resolves to the correct view.
        """
        url = reverse("api:token_refresh")
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_register_url_resolves(self):
        """
        Test register URL resolves to the correct view.
        """
        url = reverse("api:register-list")
        self.assertEqual(resolve(url).func.cls, RegisterView)

    def test_user_url_resolves(self):
        """
        Test user URL resolves to the correct view.
        """
        url = reverse("api:user-list")
        self.assertEqual(resolve(url).func.cls, UserViewSet)

    def test_todo_url_resolves(self):
        """
        Test todo URL resolves to the correct view.
        """
        url = reverse("api:todo-list")
        self.assertEqual(resolve(url).func.cls, TodoViewSet)

    def test_ws_token_url_resolves(self):
        """
        Test ws_token URL resolves to the correct view.
        """
        url = reverse("api:ws_token-list")
        self.assertEqual(resolve(url).func.cls, GetWSTokenView)
