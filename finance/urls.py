from django.urls import path
from .views import DebtArrivedCargoListView, DebtCurtomerListView, ArrivedCargoListView, CustomerListView, DashboardView


urlpatterns = [
    path("mening-qarzlarim/", DebtArrivedCargoListView.as_view(), name="debt_arrived_cargo_list"),
    path("temir-daftar/", DebtCurtomerListView.as_view(), name="debt_customer_list"),
    
    path("kelgan-mahsulotlar-ro'yxati/", ArrivedCargoListView.as_view(), name="arrivedcargo_list"),
    path("sotilgan-mahsulotlar-ro'yxati/", CustomerListView.as_view(), name="customer_list"),
    
    path("dashboard/", DashboardView.as_view(), name="dashboard")
]