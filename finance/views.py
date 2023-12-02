from django.shortcuts import render, redirect
from django.views import View
from .models import DeptArrivedCargo, DebtCustomer
from .mixins import AdminRequiredMixin
from products.models import KelganProduct, Customer
from django.utils.timezone import datetime, timedelta
from django.db.models import Sum

# Create your views here.

class DebtArrivedCargoListView(AdminRequiredMixin, View):
    def get(self, request):
        debts = DeptArrivedCargo.objects.all().select_related("cargo", "user", "cargo__user").prefetch_related("cargo__yetibkelganproduct_set", "cargo__yetibkelganproduct_set__product")
        return render(request, "debt_arrived_cargo.html", {"debts":debts})  
    
    def post(self, request):
        debt_id = request.POST.get("debt_id")
        amount = request.POST.get("amount")   
        if debt_id and amount:
            debt = DeptArrivedCargo.objects.get(id=int(debt_id))
            debt.amount -= int(amount)
            debt.payed_amount += int(amount)
            debt.save()
            return redirect("debt_arrived_cargo_list")

class DebtCurtomerListView(AdminRequiredMixin, View):
    def get(self, request):
        debts = DebtCustomer.objects.all().order_by("-id").select_related("customer", "user").prefetch_related("customer__selledproduct_set", "customer__selledproduct_set__product")
        return render(request, "debt_customer_list.html", {"debts":debts})
    
    def post(self, request):
        debt_id = request.POST.get("debt_id")
        amount = request.POST.get("amount")
        if debt_id and amount:
            debt = DebtCustomer.objects.get(id=int(debt_id))
            debt.amount -= int(amount)
            debt.payed_amount += int(amount)
            debt.save()
            return redirect("debt_customer_list")
        else:
            return redirect("debt_customer_list")
        
class ArrivedCargoListView(AdminRequiredMixin, View):
    def get(self, request):
        arrivedcargos = KelganProduct.objects.all()
        context = {"arrivedcargos": arrivedcargos}
        
        name = request.GET.get("name")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        savdo_turi = request.GET.get("savdo_turi")
        
        if name:
            arrivedcargos = arrivedcargos.filter(yetkazib_beruvci__icontains = name)
            context['arrivedcargos'] = arrivedcargos
            context['name'] = name
            
        if start_date:
            arrivedcargos = arrivedcargos.filter(datetime__gte = start_date)
            context['arrivedcargos'] = arrivedcargos
            context['start_date'] = start_date
            
        if end_date:
            arrivedcargos = arrivedcargos.filter(datetime__lte = end_date)
            context['arrivedcargos'] = arrivedcargos
            context['end_date'] = end_date
            
        if savdo_turi:
            arrivedcargos = arrivedcargos.filter(savdo_turi=savdo_turi)
            context['arrivedcargos'] = arrivedcargos
            context['savdo_turi'] = savdo_turi
            
        return render(request, "arrivedcargo_list.html", context)

class CustomerListView(AdminRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all().order_by("-id").select_related("user").prefetch_related("selledproduct_set", "selledproduct_set__product")
        context = {"customers": customers, "title":"Sotilgan Mahsulotlar"}
        name = request.GET.get("name")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        savdo_turi = request.GET.get("savdo_turi")
        
        if name:
            customers = customers.filter(name__icontains = name)
            context['customers'] = customers
            context['name'] = name
            
        if start_date:
            customers = customers.filter(datetime__gte = start_date)
            context['customers'] = customers
            context['start_date'] = start_date
            
        if end_date:
            customers = customers.filter(datetime__lte = end_date)
            context['customers'] = customers
            context['end_date'] = end_date
            
        if savdo_turi:
            customers = customers.filter(savdo_turi=savdo_turi)
            context['customers'] = customers
            context['savdo_turi'] = savdo_turi
        return render(request, "customer_list.html", context)

class DashboardView(AdminRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.filter(datetime__month=datetime.now().month)
        debtcustomer = DebtCustomer.objects.filter(created__date=datetime.now().date())
        try:
            todays_sells = Customer.objects.filter(datetime__date=datetime.now().date()).count()
            yesterday_sells = Customer.objects.filter(datetime__date=datetime.now()-timedelta(days=1)).count()
            
            farq = (todays_sells / yesterday_sells) * 100
            
            bugungi_tushum = Customer.objects.filter(datetime__date=datetime.now().date()).aggregate(Sum("amount"))
            kecagi_tushum = Customer.objects.filter(datetime__date=datetime.now().date()-timedelta(days=1)).aggregate(Sum("amount"))
            tushum_farqi = (bugungi_tushum["amount__sum"] / kecagi_tushum["amount__sum"]) * 100
        except:
           todays_sells = 0000
           farq = "--"
           bugungi_tushum = 000
           tushum_farqi = "---"
            
        context = {
            "customers":customers,
            "debtcustomer":debtcustomer,
            "todays_sells":todays_sells,
            "farq":farq,
            "bugungi_tushum":bugungi_tushum,
            "tushum_farqi":tushum_farqi,
        }
        return render(request, "dashboard.html", context)