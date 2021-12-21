from rest_framework import serializers
from .models import User, Company, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']

class CompanySerializer(serializers.ModelSerializer):
    class Meta :
        model = Company
        fields = '__all__'
        depth = 1

    def __init__(self, *args, **kwargs):
        super(CompanySerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

class ProfileSerializer(serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = '__all__'

