from api.views import EmailTokenObtainPairView, RegisterView, TodoViewSet, UserViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "api"

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"todo", TodoViewSet, basename="todo")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="token_obtain_pair"),
    path("token/obtain/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls
