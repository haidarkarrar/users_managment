from pdb import set_trace
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ex3.models import Company, Currency, Item, Supplier

# Create your views here.


class SupplierViewset(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Supplier.objects.all()

    def get_serializer_class(self):
        return self.SupplierSerializer

    class SupplierSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)

    def perform_create(self, serializer):
        Supplier.objects.create(
            name=serializer.data.get('name'),
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.name = serializer.validated_data.get('name')
        instance.save()
        return Response(status=status.HTTP_200_OK)


class CurrencyViewset(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Currency.objects.all()

    def get_serializer_class(self):
        return self.CurrencySerializer

    class CurrencySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)

    def perform_create(self, serializer):
        Currency.objects.create(
            name=serializer.data.get('name'),
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.name = serializer.validated_data.get('name')
        instance.save()
        return Response(status=status.HTTP_200_OK)


class CompanyViewset(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        return self.CompanySerializer

    class CompanySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=50)

    def perform_create(self, serializer):
        Company.objects.create(
            name=serializer.data.get('name'),
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.name = serializer.validated_data.get('name')
        instance.save()
        return Response(status=status.HTTP_200_OK)


class ItemViewset(GenericViewSet, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = Item.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return self.createItemSerializer
        if self.action == 'update':
            return self.updateItemSerializer
        if self.action == 'get_filter':
            return self.getFilterSerializer
        if self.action == 'filter_items':
            return self.getFilterSerializer
        # if self.action == 'get_filter':
        #     return self.getFilterSerializer
        # if self.action == 'retrieve':
        return self.retrieveItemSerializer

    class createItemSerializer(serializers.Serializer):

        document_date = serializers.DateField()
        balance = serializers.IntegerField()
        company = serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all())
        supplier = serializers.PrimaryKeyRelatedField(
            queryset=Supplier.objects.all())
        currency = serializers.PrimaryKeyRelatedField(
            queryset=Currency.objects.all())

        class Meta:
            fields = ['document_date', 'balance',
                      'company', 'supplier', 'currency']

    class updateItemSerializer(serializers.Serializer):
        document_date = serializers.DateField()
        balance = serializers.IntegerField()
        company = serializers.PrimaryKeyRelatedField(
            queryset=Company.objects.all())
        supplier = serializers.PrimaryKeyRelatedField(
            queryset=Supplier.objects.all())
        currency = serializers.PrimaryKeyRelatedField(
            queryset=Currency.objects.all())

    class retrieveItemSerializer(serializers.Serializer):
        document_date = serializers.DateField()
        balance = serializers.IntegerField()
        company = serializers.CharField(read_only=True)
        supplier = serializers.CharField(read_only=True)
        currency = serializers.CharField(read_only=True)

    class getFilterSerializer(serializers.Serializer):
        choices = ['company_id', 'supplier_id', 'currency_id']
        filter_by = serializers.ChoiceField(choices, write_only=True)
        filter_id = serializers.IntegerField(write_only=True)
        document_date = serializers.DateField(read_only=True)
        balance = serializers.IntegerField(read_only=True)
        company = serializers.CharField(read_only=True)
        supplier = serializers.CharField(read_only=True)
        currency = serializers.CharField(read_only=True)

    def perform_create(self, serializer):
        Item.objects.create(
            document_date=serializer.validated_data.get('document_date'),
            balance=serializer.validated_data.get('balance'),
            company=serializer.validated_data.get('company'),
            supplier=serializer.validated_data.get('supplier'),
            currency=serializer.validated_data.get('currency'),
        )
        return Response(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = self.get_object()
        instance.document_date = serializer.validated_data.get('document_date')
        instance.balance = serializer.validated_data.get('balance')
        instance.company = serializer.validated_data.get('company')
        instance.supplier = serializer.validated_data.get('supplier')
        instance.currency = serializer.validated_data.get('currency')
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='get-filter')
    def get_filter(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        filter_by = serializer.validated_data.get('filter_by')
        filter_id = serializer.validated_data.get('filter_id')
        return Response(self.filter_items(request, kwargs={'filter_by': filter_by, 'filter_id': filter_id}).data)

    @action(detail=False, methods=['get'], url_path='filter-items')
    def filter_items(self, request, kwargs):
        filter_by = kwargs['filter_by']
        filter_id = kwargs['filter_id']
        if filter_by == 'company_id':
            queryset = Item.objects.filter(company_id=filter_id)
        if filter_by == 'supplier_id':
            queryset = Item.objects.filter(supplier_id=filter_id)
        if filter_by == 'currency_id':
            queryset = Item.objects.filter(currency_id=filter_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
