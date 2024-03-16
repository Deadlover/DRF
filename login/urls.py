from django.urls import path
from . import views

urlpatterns = [
    path('',views.LoginPage.as_view(),name='Loginpage'),
    path('signup/',views.SignupPage.as_view(),name='Signup'),
]