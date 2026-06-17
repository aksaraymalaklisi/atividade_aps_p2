from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.presentation.views import (
    AuthenticateUserView,
    RegisterUserView,
    UserProfileView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", AuthenticateUserView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
