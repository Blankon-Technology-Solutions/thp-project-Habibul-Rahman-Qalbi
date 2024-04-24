from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import CustomUser, UserTodo
from api.serializers import (
    TodoSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
    RegisterSerializer,
)
from backend.permissions import IsAdmin, IsOwner, IsUser
from rest_framework.mixins import CreateModelMixin


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class LinkedInLogin(SocialLoginView):
    adapter_class = LinkedInOAuth2Adapter


class LinkedInConnect(SocialConnectView):
    adapter_class = LinkedInOAuth2Adapter


class RegisterView(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = UserTodo.objects.all()
    permission_classes = [IsOwner]


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdmin | IsUser]
