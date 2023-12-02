from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import ProductForm, KelganProductForm, YetibkelganProductFormset, CustomerForm, SelledProductFormset
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Customer, Category
from django.http import HttpResponse 
from django.contrib import messages
from django.utils.timezone import datetime
from finance.mixins import AdminRequiredMixin
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            return redirect("dashboard")
        return render(request, "sell_product")

class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, "create.html", {"form":form})
    
    def post(self, request):
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            form.save()
            return redirect("list")
        else:
            return render(request, "create.html", {"form":form})

class ProductListView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        
        context = {"products":products, "categories":Category.objects.all()}
        
        q = request.GET.get("q")
        category_id = request.GET.get("category")
        if q:
            products = Product.objects.filter(name__icontains=q)
            context['products'] = products
            context['category_id'] = category_id
            
        if category_id:
            # category = Category.objects.get(id=int(category_id))
            print(category_id)
            products = products.filter(category__id=int(category_id))
            context['products'] = products
            context['category_id'] = int(category_id)
            
        return render(request, "list.html", context)

class ProductDetailView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return HttpResponse(product.name)

class ProductUpdateView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        form = ProductForm(instance=product)
        return render(request, "update.html", {"form":form, "product":product})
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("list")
        else:
            return render(request, "update.html", {"form":form, "product":product})

class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        return render(request, "delete.html", {'product':product})
        
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        product_name = request.POST.get("product_name")
        if product_name == product.name:
            product.delete()
            return redirect("list")
        else:
            return HttpResponse("Error") 
            # return render(redirect, "delete.html", {'product':product})

class ProductKelganYukView(LoginRequiredMixin, View):
    def get(self, request):
        form = KelganProductForm() 
        formset = YetibkelganProductFormset()
        return render(request, "arrived_cargo.html", {"form":form, 'formset':formset})
    
    def post(self, request):
        form = KelganProductForm(data=request.POST) 
        if form.is_valid():
            arrivedcargo = form.save(commit=False)
            arrivedcargo.user = request.user
            formset = YetibkelganProductFormset(instance=arrivedcargo, data=request.POST)
            if formset.is_valid():
                form.save()
                formset.save()
                form.save()
            # for i in range(7):
            #     product_id = request.POST.gte(f"arrivedproduct_set-{i}-product")
            #     quantity = request.POST.get(f"arrivedproduct_set-{i}-quantity")
            #     if quantity and product_id:
            #         product = Product.objects.get(id=int(product_id))
            #         KelganProduct.objects.create(product=product, quantity=quantity, cargo=arrivedcargo)
            
                return redirect("list")
        
        return render(request, "arrived_cargo.html", {"form":form, 'formset':formset})
    
class ProductSellView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerForm()
        formset = SelledProductFormset()
        return render(request, "sell_product.html", {'form':form, 'formset':formset})
    
    def post(self, request):
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            formset = SelledProductFormset(instance=customer, data=request.POST)
            if formset.is_valid():
                form.save()
                formset.save()
                form.save()
                messages.success(request, "Mahsulot muvaffaqiyatli sotildi")
                return redirect("customer_detail", customer.id)
        
        return render(request, "sell_product.html", {"form":form, 'formset':formset})

class CustomerDetail(LoginRequiredMixin, View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        return render(request, "customer_detail.html", {"customer":customer})

class TodaysSellsView(LoginRequiredMixin, View):
    def get(self, request):
        today =  datetime.today()
        customers = Customer.objects.filter(datetime__year=today.year, datetime__month=today.month, datetime__day=today.day, user=request.user)
        return render(request, "customer_list.html", {"customers":customers, "title":"Bugungi Savdoyingiz"})