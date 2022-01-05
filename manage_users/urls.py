from django.urls import path
from django.urls.conf import include
from .views import UserViewset, CompanyViewset, ProfileViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewset, basename='user')
router.register('company', CompanyViewset, basename='company')
router.register('profile', ProfileViewset, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>', include(router.urls)),
]
