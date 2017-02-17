# -*- coding: UTF-8 -*-

from django.db import models
import sys
from django.contrib.auth.models import User
from tastypie.models import ApiKey

reload(sys)
sys.setdefaultencoding("utf8")
'''
def createApiKey():
    if len(ApiKey.objects.filter(key = '1a23'))==0:
        ApiKey.objects.create(key='1a23', user=User.objects.get(id = 1))

createApiKey()
'''
class Invoice(models.Model):
    Photo = models.CharField(max_length=1000, db_column="Photo", null=False)
    DateTime = models.DateTimeField(db_column="DateTime", null=False)
    User = models.ForeignKey(User)

    class Meta:
        db_table = 'Invoice'

class Shop(models.Model):
    Name = models.CharField(max_length=100, db_column="Name", null=False)
    Address = models.CharField(max_length=100, db_column="Address", null=False)

    class Meta:
        db_table = 'Shop'

    def __str__(self):
        return self.Name

class Product(models.Model):
    Title = models.CharField(max_length=100, db_column="Title", null=False, verbose_name="Назва")
    Description = models.TextField(db_column="Description", null=False, verbose_name="Опис")
    Photo = models.ImageField(db_column="Photo", null=False, verbose_name="Фото")
    Price = models.FloatField(db_column="Price", null=False, verbose_name="Ціна")

    class Meta:
        db_table = 'Product'

    def __str__(self):
        return self.Title

class SendToShop(models.Model):
    User_id = models.ForeignKey(User)
    Shop_id = models.ForeignKey(Shop)
    DateTime = models.DateTimeField(db_column="DateTime", null=False)

    class Meta:
        db_table = 'SendToShop'

    def __str__(self):
        return self.Shop_id.__str__() + ": " + self.DateTime.__str__()

class ProductToShop(models.Model):
    Product_id = models.ForeignKey(Product)
    SendToShop_id = models.ForeignKey(SendToShop)

    class Meta:
        db_table = 'ProductToShop'

class Sale(models.Model):
    DateTime = models.DateTimeField(db_column="DateTime", null=False)
    User_id = models.ForeignKey(User)

    class Meta:
        db_table = 'Sale'

class BarCode(models.Model):
    ProductToShop_id = models.ForeignKey(ProductToShop)
    SoldOut = models.BooleanField(db_column="SoldOut", null=False, default=False, verbose_name="Реалізовано")
    Sale_id = models.ForeignKey(Sale, null=True)

    class Meta:
        db_table = 'BarCode'

class Revision(models.Model):
    DateTime = models.DateTimeField(db_column="DateTime", null=False)
    User_id = models.ForeignKey(User)

    class Meta:
        db_table = 'Revision'

class RevisionHasBarCode(models.Model):
    Revision_id = models.ForeignKey(Revision)
    BarCode = models.ForeignKey(BarCode)
    OK = models.BooleanField(db_column="OK", null=False, default=False, verbose_name="Наявно")

    class Meta:
        db_table = 'RevisionHasBarCode'