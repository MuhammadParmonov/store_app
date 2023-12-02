from django.contrib import admin
from .models import DeptArrivedCargo, DebtCustomer
# Register your models here.


admin.site.register([DeptArrivedCargo, DebtCustomer])