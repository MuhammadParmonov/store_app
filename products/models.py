from django.db import models
from users.models import User
# Create your models here.

OLCHOV_USULI = (
    ("kg", "Kilogram"),
    ("metr", "Metr"),
    ("pc", "Dona"),
    ("litr", "Litr"),
)

SOTUV_USULI = (
    ("qarz","Nasiya"),
    ("naqt","Naqt"),
)

TYPE_OF_PRICE = (
    ("selling","Sotilish Narxi"),
    ("wholesale","Optom Narxi"),
    ("actual","Haqiqiy Narxi"),
)

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    olingan_price = models.PositiveBigIntegerField(help_text="Mahsulotni olib kelingan narxi")
    sotuv_price = models.PositiveBigIntegerField(help_text="Mahsulotni sotilish narxi")
    optom_price = models.PositiveBigIntegerField(help_text="Mahsulotni optom narxi")
    olchov_usuli = models.CharField(max_length=5, choices=OLCHOV_USULI)
    soni = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name}, {self.soni} {self.olchov_usuli} qolgan"
    
class KelganProduct(models.Model):
    yetkazib_beruvci = models.CharField(max_length=150, verbose_name="Yetkazib beruvchi")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    savdo_turi = models.CharField(max_length=50, choices=SOTUV_USULI, verbose_name='Savdo turi')
    amount = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return str(self.yetkazib_beruvci)

class YetibkelganProduct(models.Model):
    cargo = models.ForeignKey(KelganProduct, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    soni = models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.Product.name)

class Customer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Sotib oluvchi", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField(default=0)
    savdo_turi = models.CharField(max_length=50, choices=SOTUV_USULI, verbose_name='Savdo turi')
    
    def __str__(self):
        return str(self.name)

class SelledProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    soni = models.PositiveIntegerField()
    type_of_price = models.CharField(max_length=25, choices=TYPE_OF_PRICE)
    
    def __str__(self):
        return str(self.product.name)