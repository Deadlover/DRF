from django.urls import path,include
from . import views

urlpatterns = [
    path('menu/',views.MenuApi.as_view(),name='menu'),
    path('category/',views.CategoryApi.as_view(),name='category'),
    path('upload/',views.UploadApi.as_view(),name='upload'),
    path('cart/',views.Add_To_CartApi.as_view(),name='cart'),
]