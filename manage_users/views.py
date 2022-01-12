from pdb import set_trace
from user_management.settings import EMAIL_HOST_USER
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from django.contrib.auth.hashers import make_password
from .models import Company, Profile, User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

# Create your views here.


class UserViewset(GenericViewSet, RetrieveModelMixin, CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin):
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
        if self.action == 'request_reset_password_email':
            return self.ResetPasswordEmailRequestSerializer
        if self.action == 'change_activation_status':
            return self.ActivationStatusSerializer
        if self.action == 'set_new_password':
            return self.SetNewPasswordSerializer

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
            style={'input_type': 'password', 'placeholder': 'Password'}
        )
        phone_number = serializers.CharField(max_length=12)

    class updateUserSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150, required=False)
        first_name = serializers.CharField(max_length=150, required=False)
        last_name = serializers.CharField(max_length=150, required=False)
        email = serializers.EmailField(required=False)
        phone_number = serializers.CharField(max_length=12, required=False)

    class retrieveUserSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        first_name = serializers.CharField(max_length=150)
        last_name = serializers.CharField(max_length=150)
        email = serializers.EmailField()
        phone_number = serializers.CharField(max_length=12)
        date_joined = serializers.DateTimeField()
        is_active = serializers.BooleanField()
        is_staff = serializers.BooleanField()
        is_deleted = serializers.BooleanField()

    class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        old_password2 = serializers.CharField(required=True)
        new_password = serializers.CharField(
            required=True, min_length=6, max_length=20)

    class ActivationStatusSerializer(serializers.Serializer):
        is_active = serializers.BooleanField()

    class ResetPasswordEmailRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    class SetNewPasswordSerializer(serializers.Serializer):
        password = serializers.CharField(min_length=6, max_length=20)

    def perform_create(self, serializer):
        User.objects.create(
            username=serializer.data.get('username'),
            first_name=serializer.data.get('first_name'),
            last_name=serializer.data.get('last_name'),
            email=serializer.data.get('email'),
            password=make_password(serializer.data.get('password')),
            phone_number=serializer.data.get('phone_number'),
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.username = serializer.validated_data.get('username')
        instance.first_name = serializer.validated_data.get('first_name')
        instance.last_name = serializer.validated_data.get('last_name')
        instance.email = serializer.validated_data.get('email')
        instance.phone_number = serializer.validated_data.get('phone_number')
        instance.save()
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='request-reset-email', url_name='request-reset-email')
    def request_reset_password_email(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = self.get_object()
        if email == user.email:
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = '/user/' + str(user.id) + '/password-reset/' + token
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello \n Use link below to reset your password \n' + absurl
            subject = 'Reset your password'
            send_mail(subject, email_body, EMAIL_HOST_USER, [
                      'haidaralkarrar17@gmail.com'], fail_silently=False)

            return Response({'success': 'we have sent you an email'}, status=status.HTTP_200_OK)
        return Response({'failed': 'email does not match'}, status=status.HTTP_404_NOT_FOUND)

    # @action(detail=True, methods=['get'], url_path=r'password-reset/(?P<token>\w+)', url_name='password-reset-confirm')
    @action(detail=True, methods=['patch'], url_path='password-reset/az569s-6ad4e11c2f56aa496128bc1c923486cb', url_name='password-reset-confirm')
    def set_new_password(self, request, pk):
        user = self.get_object()
        if not PasswordResetTokenGenerator().check_token(user, 'az569s-6ad4e11c2f56aa496128bc1c923486cb'):
            return Response({'error': 'Token is not valid'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get('password')
        user.set_password(password)
        user.save()

        return Response({'success': 'success'})

    @action(detail=True, methods=['put'], url_path='change-activation-status')
    def change_activation_status(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.is_active = serializer.data.get('is_active')
        instance.save()
        if instance.is_active:
            message = 'user activated'
        else:
            message = 'user deactivated'
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': message,
            'data': []
        }
        return Response(response)

    @action(detail=True, methods=['put'], url_path='change-password')
    def change_password(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('old_password') == serializer.data.get('old_password2'):
                if not instance.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                instance.set_password(serializer.data.get("new_password"))
                instance.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewset(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    class CompanySerializer(serializers.ModelSerializer):
        users = UserViewset.listUsersSerializer(many=True, read_only=True)

        class Meta:
            model = Company
            fields = ['id', 'name', 'city', 'users']

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class ProfileViewset(GenericViewSet, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin):
    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = '__all__'

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
