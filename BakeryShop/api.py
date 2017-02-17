from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from django.contrib.auth.models import User
from models import SendToShop, BarCode, Invoice, Product, Shop, ProductToShop
from tastypie import fields

MAX_LIMIT = 10000

class UserApi(ModelResource):
    class Meta:
        max_limit = MAX_LIMIT
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class InvoiceApi(ModelResource):
    user = fields.ForeignKey(UserApi, 'User')

    class Meta:
        max_limit = MAX_LIMIT
        queryset = Invoice.objects.all()
        resource_name = 'invoice'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class ProductApi(ModelResource):
    class Meta:
        max_limit = MAX_LIMIT
        queryset = Product.objects.all()
        resource_name = 'product'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class ShopApi(ModelResource):
    class Meta:
        max_limit = MAX_LIMIT
        queryset = Shop.objects.all()
        resource_name = 'shop'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class SendToShopApi(ModelResource):
    user = fields.ForeignKey(UserApi, 'User_id')
    shop = fields.ForeignKey(ShopApi, 'Shop_id')

    class Meta:
        max_limit = MAX_LIMIT
        queryset = SendToShop.objects.all()
        resource_name = 'send_to_shop'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class ProductToShopApi(ModelResource):

    product = fields.ForeignKey(ProductApi, 'Product_id')
    sendToShop = fields.ForeignKey(SendToShopApi, 'SendToShop_id')

    class Meta:
        max_limit = MAX_LIMIT
        queryset = ProductToShop.objects.all()
        resource_name = 'product_to_shop'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict

class BarCodeApi(ModelResource):

    productToShop = fields.ForeignKey(ProductToShopApi, 'ProductToShop_id')

    class Meta:
        max_limit = MAX_LIMIT
        queryset = BarCode.objects.all()
        resource_name = 'barcode'
        authorization = Authorization()
        authentication = BasicAuthentication()

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del (data_dict['meta'])
                return data_dict
