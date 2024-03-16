from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .renderers import UserRenderer
from .serializer import UserLogin,UserSignUP
from rest_framework.response import Response
from rest_framework import status 



# FOR TOKEN GENERATION
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginPage(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request,format=None):
        serializer = UserLogin(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            token = get_token_for_user(user)
            return Response({'token':token,'msg':'login success'},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['email or password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        

class SignupPage(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request,format=None):
        serializer = UserSignUP(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_token_for_user(user)
        return Response({'token':token,'msg':'registration success '},status=status.HTTP_201_CREATED)


