from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", views.LoginPage.as_view(), name="Loginpage"),
    path("signup/", views.SignupPage.as_view(), name="Signup"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
