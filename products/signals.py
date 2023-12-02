from .models import Product, Category, KelganProduct, YetibkelganProduct, SelledProduct
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from slugify import slugify


@receiver(pre_save, sender=Product)
def update_product_slug(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
    

@receiver(pre_save, sender=Category)
def update_category_slug(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


@receiver(post_save, sender=YetibkelganProduct)
def add_quantity(instance, created, *args, **kwargs):
    if created:
        product = instance.product
        product.soni += int(instance.soni)
        product.save()

@receiver(post_save, sender=SelledProduct)
def minus_quantity(instance, created, *args, **kwargs):
    if created:
        product = instance.product
        product.soni -= int(instance.soni)
        product.save()