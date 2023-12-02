from django.contrib import admin
from .models import Category, Product, KelganProduct, YetibkelganProduct, Customer, SelledProduct
from import_export.admin import ImportExportModelAdmin
# Register your models here. 

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ["name", "soni", "olchov_usuli", "sotuv_price", "optom_price", "olingan_price", "created_at", "update_at"]
    search_field = ["name"]
    list_filter = ["category"]


admin.site.register([Category, KelganProduct, YetibkelganProduct, SelledProduct])