from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from products.models import KelganProduct, Customer
from .models import DeptArrivedCargo, DebtCustomer
from products.models import SelledProduct

@receiver(pre_save, sender=KelganProduct)
def calculate_arrivedcargo(instance, *args, **kwargs):
    
    try:
        arrived_product = instance.yetibkelganproduct_set.all()
        amount = 0
        for i in arrived_product:
            price = i.product.olingan_price
            quantity = i.soni
            amount += (price*quantity)
            
        instance.amount = amount
        
    except:
        pass

@receiver(post_save, sender=KelganProduct)
def check_arrived_cargo_payment(instance, *args, **kwargs):
    if instance.savdo_turi == "qarz":
        debt, created = DeptArrivedCargo.objects.get_or_create(cargo=instance, user=instance.user)
        debt.amount = instance.amount
        debt.save()

@receiver(pre_save, sender=Customer)
def calculate_customer_amount(instance, *args, **kwargs):
    try:
        selled_products = instance.selledproduct_set.all()
        amount = 0
        for i in selled_products:
            if i.type_of_price == 'selling':
                price = i.product.olingan_price
            elif i.type_of_price == 'actual':
                price = i.product.sotuv_price
            else:
                price = i.product.optom_price
                
            quantity = i.soni
            amount += (price*quantity)
            
        instance.amount = amount
    except:
        print("No More")

@receiver(post_save, sender=Customer)
def check_pyment_type_customer(instance, *args, **kwargs):
    if instance.savdo_turi == "qarz":
        debt, created = DebtCustomer.objects.get_or_create(customer=instance, user=instance.user)
        debt.amount = instance.amount
        debt.save()

