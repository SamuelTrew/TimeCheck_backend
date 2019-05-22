from django.urls import path

from .views import CurrentUserView, UserLoginView, UserLogoutView

app_name = "users"

urlpatterns = [
    path("me", CurrentUserView.as_view(), name="detail"),
    path("login", UserLoginView.as_view(), name="login"),
    path("logout", UserLogoutView.as_view(), name="logout"),
]