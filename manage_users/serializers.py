from rest_framework import serializers
from .models import User, Company, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number']

class CompanySerializer(serializers.ModelSerializer):

    users = UserSerializer(many=True, read_only=True)    
    class Meta :
        model = Company
        fields = ['id', 'name', 'city', 'users']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = '__all__'

