from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.hashers import make_password
from .models import Company, Profile, User

# Create your views here.

class UserViewset(ModelViewSet, RetrieveModelMixin):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return self.listUsersSerializer
        if self.action == 'create':
            return self.createUsersSerializer
        if self.action == 'retrieve':
            return self.retrieveUserSerializer
        if self.action == 'update':
            return self.updateUserSerializer
        if self.action == 'change_password':
            return self.ChangePasswordSerializer
        if self.action == 'reset_password':
            return self.ResetPasswordSerializer
        return self.listUsersSerializer


    class listUsersSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        phone_number = serializers.CharField(max_length=12)
    class createUsersSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        password = serializers.CharField(
            write_only=True,
            required=True,
            style={'input_type': 'password', 'placeholder': 'Password'}
        )
        phone_number = serializers.CharField(max_length=12)
    
    class updateUserSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        phone_number = serializers.CharField(max_length=12)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.email = validated_data.get('email', instance.email)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.save()
            return instance

    class retrieveUserSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        phone_number = serializers.CharField(max_length=12)
        date_joined = serializers.DateTimeField()
        is_active = serializers.BooleanField()
        is_staff = serializers.BooleanField()

    class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

    class ResetPasswordSerializer(serializers.Serializer):
        pass
        # new_password = serializers.CharField(read_only=True)


    def list(self, request):
        queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        user = User.objects.create(username = data['username'], first_name = data['first_name'], last_name = data['last_name'], email = data['email'], password = make_password(data['password']), phone_number = data['phone_number'])
        serializer = self.get_serializer(data = user)
        if serializer.is_valid():
            self.perform_create(serializer)
        return Response(serializer.data)
    
    def update(self, request, id):
        user = User.objects.get(id=id)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def change_password(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def reset_password(self, request, pk=None):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            object.set_password('pass123')
            object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'new password is password123',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def deactivate_user(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'user deactivated',
                    'data': []
                }
            return Response(response)
        except user.DoesNotExist:
            response = {
                    'status': 'failed',
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'user does not exist',
                    'data': []
                }
            return Response(response)
        
    @action(detail=True, methods=['put'])
    def activate_user(self, request, pk=None):
        try:
            user = self.get_object()
            user.is_active = True
            user.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'user activated',
                    'data': []
                }
            return Response(response)
        except user.DoesNotExist:
            response = {
                    'status': 'failed',
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'user does not exist',
                    'data': []
                }
            return Response(response)
        


class CompanyViewset(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    class CompanySerializer(serializers.ModelSerializer):
        users = UserViewset.listUsersSerializer(many=True, read_only=True)
        class Meta :
            model = Company
            fields = ['id', 'name', 'city', 'users']

    serializer_class = CompanySerializer
    queryset = Company.objects.all()

class ProfileViewset(GenericViewSet, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin):
    class ProfileSerializer(serializers.ModelSerializer):
        class Meta :
            model = Profile
            fields = '__all__'

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()