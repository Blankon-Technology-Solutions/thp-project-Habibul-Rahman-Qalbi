from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.linkedin_oauth2.views import LinkedInOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from sesame.utils import get_token

from api.models import CustomUser, UserTodo
from api.serializers import (
    RegisterSerializer,
    TodoSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
)
from backend.permissions import IsAdmin, IsAuthenticated, IsOwner, IsUser


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


class GetWSTokenView(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        token = get_token(user)
        return Response({"ws_token": token})


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = UserTodo.objects.all()
    permission_classes = [IsOwner]


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdmin | IsUser]
