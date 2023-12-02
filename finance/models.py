from django.db import models
from users.models import User
from products.models import Product, KelganProduct, YetibkelganProduct, Customer
from django.utils import timezone 
# Create your models here.

class DeptArrivedCargo(models.Model):
    cargo = models.OneToOneField(KelganProduct, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payed_amount = models.PositiveBigIntegerField(default=0)
    
    @property
    def is_payed(self):
        return True if self.amount == 0 else False
    
    @property
    def is_late(self):
        return True if timezone.now() - self.created > timezone.timedelta(days=31) else False
    
    def __str__(self):
        return str(self.amount)

class DebtCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payed_amount = models.PositiveBigIntegerField(default=0)
    
    @property
    def is_payed(self):
        return True if self.amount == 0 else False
    
    @property
    def is_late(self):
        return True if timezone.now() - self.created > timezone.timedelta(days=31) else False