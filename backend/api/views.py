from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, TokenObtainPairSerializer, TodoSerializer
from .models import CustomUser, UserTodo
from backend.permissions import IsUser, IsAdmin, IsOwner


class RegisterView(APIView):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={"errors": serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = UserTodo.objects.all()
    permission_classes = [IsOwner]


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdmin, IsUser]
