from django.shortcuts import render
from rest_framework import viewsets, mixins

from manage_users import serializers
from .models import Company, Profile, User

from manage_users.serializers import CompanySerializer, ProfileSerializer, UserSerializer

# Create your views here.

class UserViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CompanyViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class ProfileViewset(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()