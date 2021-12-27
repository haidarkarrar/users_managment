from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin


from .models import Company, Profile, User

from manage_users.serializers import CompanySerializer, ProfileSerializer, UserSerializer

# Create your views here.

class UserViewset(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class CompanyViewset(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class ProfileViewset(viewsets.GenericViewSet, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()