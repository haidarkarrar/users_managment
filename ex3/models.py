from django.db import models

# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    document_date = models.DateField()
    balance = models.IntegerField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company')
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name='currency')
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name='supplier')

    def __int__(self):
        return self.id
