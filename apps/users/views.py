from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.users.models import User
from apps.users.serializer import UserSerializer, UserRegisterSerializer


class UserAPIList(GenericViewSet,
                  mixins.ListModelMixin):
    
    


# Create your views here.
