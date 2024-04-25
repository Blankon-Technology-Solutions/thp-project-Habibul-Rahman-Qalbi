from api.models import CustomUser, UserTodo
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JwtTokenObtainPairSerializer,
)


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ["password"]


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
            "first_name",
            "last_name",
            "password",
            "password2",
            "email",
        )
        extra_kwargs = {
            "first_name": {
                "allow_blank": True,
                "help_text": _("Insert user first name"),
            },
            "last_name": {"allow_blank": True, "help_text": _("Insert user last name")},
        }

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": _("Password fields didn't match.")})

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,
        )


class TodoSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserTodo
        fields = "__all__"

    # Make sure to only create user's own todo
    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if isinstance(request.user, CustomUser):
                validated_data["user"] = request.user
        return super().create(validated_data)

    # Make sure to only update user's own todo
    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if isinstance(request.user, CustomUser):
                validated_data["user"] = request.user
        return super().update(instance, validated_data)
