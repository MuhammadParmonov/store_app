from .models import Product, Category, KelganProduct, YetibkelganProduct, Customer, SelledProduct
from django.forms import ModelForm, inlineformset_factory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "image",
            "olingan_price",
            "sotuv_price",
            "optom_price",
            "olchov_usuli",
        ]

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        
class KelganProductForm(ModelForm):
    class Meta:
        model = KelganProduct
        fields = ["yetkazib_beruvci", "savdo_turi"]
        
class YetibkelganProductForm(ModelForm):
    class Meta:
        model = YetibkelganProduct
        fields = ["product", "soni"]

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'savdo_turi']

class SelledProductForm(ModelForm):
    class Meta:
        model = SelledProduct
        fields = ['product', 'soni', 'type_of_price']


SelledProductFormset = inlineformset_factory(Customer, SelledProduct, form=SelledProductForm, fields=['product', 'soni', 'type_of_price'], extra=7)
YetibkelganProductFormset = inlineformset_factory(KelganProduct, YetibkelganProduct, form=YetibkelganProductForm, fields=['product', 'soni'], extra=7)