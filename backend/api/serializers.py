from .models import UserTodo, CustomUser
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JwtTokenObtainPairSerializer,
)


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password")


class RegisterSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        help_text=_("Insert your Email Address"),
        validators=[UniqueValidator(queryset=CustomUser.objects.all()), validate_email],
    )
    password = CharField(
        write_only=True,
        required=True,
        validators=[],
        help_text=_("Insert password for this user account"),
    )
    password2 = CharField(
        write_only=True,
        required=True,
        help_text=_("Confirm password for this user account"),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "password2",
            "email",
        )
        extra_kwargs = {
            "username": {"help_text": _("Insert username for this account")},
            "first_name": {"required": True, "help_text": _("Insert user first name")},
            "last_name": {"allow_blank": True, "help_text": _("Insert user last name")},
        }

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": _("Password fields didn't match.")})

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,
        )


class TodoSerializer(ModelSerializer):
    class Meta:
        model = UserTodo
        fields = "__all__"