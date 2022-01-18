from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from ex3.views import CompanyViewset, CurrencyViewset, ItemViewset, SupplierViewset

router = DefaultRouter()
router.register('supplier', SupplierViewset, basename='supplier')
router.register('currency', CurrencyViewset, basename='currency')
router.register('company', CompanyViewset, basename='company')
router.register('item', ItemViewset, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>', include(router.urls)),
]
