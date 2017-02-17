from django.forms import ModelForm
from models import Shop, Product

class ShopForm(ModelForm):
    class Meta:

        model = Shop
        fields = ['Name', 'Address']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'