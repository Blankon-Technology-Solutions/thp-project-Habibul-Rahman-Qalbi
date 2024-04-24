from django.urls import path
from rest_framework.routers import DefaultRouter
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

app_name = "api"

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"todo", TodoViewSet, basename="todo")
router.register(r"register", RegisterView, basename="register")
router.register(r"ws_token", GetWSTokenView, basename="ws_token")

urlpatterns = [
    path("login/google/", GoogleLogin.as_view(), name="google_login"),
    path("login/linkedin/", LinkedInLogin.as_view(), name="linkedin_login"),
    path("connect/google/", GoogleConnect.as_view(), name="google_connect"),
    path("connect/linkedin/", LinkedInConnect.as_view(), name="linkedin_connect"),
    path("token/obtain/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls
