from django.shortcuts import render
from django.contrib.auth.models import User
from authentication.models import User_Personal,Area
from rest_framework.views import APIView
from authentication.serializers import (
    UserSerializer,UserProfileSerializer
    )
from rest_framework.response import Response
from rest_framework import viewsets,status
# Create your views here.

class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format='json'):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user=user_serializer.save()

            if user:
                serializer = UserSerializer(instance=user)
                return Response(user.username,status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)