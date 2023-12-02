from users.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings

from .models import Category, Product, KelganProduct, YetibkelganProduct, SelledProduct, Customer
from finance.models import DebtCustomer 

import random


@override_settings(MEDIA_ROOT=settings.BASE_DIR.joinpath("test_media"))
class ProductCreationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="muhammadali", email="mm@mm.mm", password="my_pass")
        self.category = Category.objects.create(name="O'yinchoqlar")
        
        prdoucts = ['olma', 'anor', 'behi', 'olcha']
        for i in prdoucts:
            Product.objects.create(
                name=i,
                category=self.category,
                user=self.user,
                image="meva.jpg",
                olingan_price=random.randint(10000, 30000),
                sotuv_price=random.randint(10000, 30000),
                optom_price=random.randint(10000, 30000),
                olchov_usuli="kg",
                soni=5
            )

    def test_model_creation(self):
        
        Product.objects.create(
            name="Pepsi",
            category = self.category,
            user = self.user,
            image="pepsi.png",
            olingan_price = 9000,
            sotuv_price = 9000,
            optom_price = 9000,
            olchov_usuli = "pc",
            soni = 5
        )
        
        product = Product.objects.get(id=5)
        
        self.assertEqual(product.name, "Pepsi")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.user, self.user) 
        self.assertEqual(product.image, "pepsi.png")
        self.assertEqual(product.olingan_price, 9000)
        self.assertEqual(product.sotuv_price, 9000)
        self.assertEqual(product.optom_price, 9000)
        self.assertEqual(product.olchov_usuli, "pc")
        self.assertEqual(product.soni, 5)

    def test_product_create_view(self):
        self.client.login(username="muhammadali", password="my_pass")
        # ularni aniqlab olish
        url = reverse("create")
        # post request jonatish
        image = open(f"{settings.BASE_DIR}\\media\\default_user.png", "rb")
        response = self.client.post(url, {
            "name":"Non",
            "category":self.category.id,
            "image":image,
            "olingan_price":3000,
            "sotuv_price":3500,
            "optom_price":2500,
            "olchov_usuli":"pc",
        })
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(name="Non")
        self.assertEqual(self.user, product.user)

    def test_product_update_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user = self.user,
            image="pepsi.png",
            olingan_price = 9000,
            sotuv_price = 9000,
            optom_price = 9000,
            olchov_usuli = "pc",
            soni = 5
        )
        url = reverse("update", args={product.id})
        self.client.login(username="muhammadali", password="my_pass")
        image = open(f"{settings.BASE_DIR}\\media\\default_user.png", "rb") 
        
        context = {
            "name":"Pepsi 1.5l",
            "category":self.category.id,
            "image": image,
            "olingan_price":9000,
            "sotuv_price":1200,
            "optom_price":1000,
            "olchov_usuli":"pc",
            "soni":101,
        }
        
        response = self.client.post(url, context)
        
        product = Product.objects.get(name="Pepsi 1.5l")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(product.olingan_price, 9000)
        self.assertEqual(product.id, 5)
        self.assertNotEqual(product.soni, 101)
        
        User.objects.create_user(username="abubakir", email="aa@aa.aa", password="abubandit")
        self.client.login(username="abubakir", password="abubandit")
        response2 = self.client.post(url, context)
        self.assertEqual(response2.status_code, 404)
    
    def test_product_detail_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user = self.user,
            image="pepsi.png",
            olingan_price = 9000,
            sotuv_price = 9000,
            optom_price = 9000,
            olchov_usuli = "pc",
            soni = 5
        )
        self.client.login(username="muhammadali", password="my_pass")
        url = reverse("detail", args={product.id})
        response = self.client.get(url)
    
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Pepsi")
                
    def test_product_delete_view(self):
        product = Product.objects.create(
            name="Pepsi",
            category = self.category,
            user = self.user,
            image="pepsi.png",
            olingan_price = 9000,
            sotuv_price = 9000,
            optom_price = 9000,
            olchov_usuli = "pc",
            soni = 5
        )
        self.client.login(username="muhammadali", password="my_pass")
        url = reverse("delete", args={product.id})
        response = self.client.post(url, {"product_name":"nfei"})
        self.assertEqual(Product.objects.all().count(), 5)
        self.assertContains(response, "Error")
        
        response2 = self.client.post(url, {"product_name":"Pepsi"})
        self.assertEqual(Product.objects.all().count(), 4)
        self.assertEqual(response2.url, "/list/")
    
class ArrivedProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reyn', password='my_pass', email="aa@a.s")
        self.category = Category.objects.create(name="Oziq-ovqat")
        
        products = ['olma', 'anor', 'behi', 'nok']
        for i in products:
            Product.objects.create(
                name=i,
                category = self.category,
                user = self.user,
                image="meva.png",
                olingan_price = random.randint(10000, 30000),
                sotuv_price = random.randint(10000, 30000),
                optom_price = random.randint(10000, 30000),
                olchov_usuli = "kg",
                soni = 5
            )
            
    def test_arrivedproduct_creatin(self):
        self.client.login(username="reyn", password="my_pass")
        url = reverse("kelgan_yuk")

        context = {
            "yetkazib_beruvci":"Alibaba",
            "savdo_turi":"naqt",
            "yetibkelganproduct_set-TOTAL_FORMS":'7',
            "yetibkelganproduct_set-INITIAL_FORMS":'0',
            "yetibkelganproduct_set-MIN_NUM_FORMS":'0',
            "yetibkelganproduct_set-MAX_NUM_FORMS":'1000',
            "yetibkelganproduct_set-0-product":1,
            "yetibkelganproduct_set-0-soni":'150',
            "yetibkelganproduct_set-1-product":2,
            "yetibkelganproduct_set-1-soni":10,
            "yetibkelganproduct_set-2-product":3,
            "yetibkelganproduct_set-2-soni":5,
        }
        
        response = self.client.post(url, context)
        print(response.content)
        self.assertEqual(response.status_code, 302)
        arrivedcargo = KelganProduct.objects.get(yetkazib_beruvci="Alibaba")
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        product3 = Product.objects.get(id=3)
        
        self.assertEqual(product1.soni, 155)
        self.assertEqual(product2.soni, 15)
        self.assertEqual(product3.soni, 10)
    
        self.assertEqual(arrivedcargo.user, self.user)

class CustomerHammasiTastCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", email="mm@mm.mm", password="my_pass", is_superuser=True)
        self.category = Category.objects.create(name="O'yinchoqlar")
       
        prdoucts = ['olma', 'anor', 'behi', 'olcha']
        for i in prdoucts:
            Product.objects.create(
                name=i,
                category=self.category,
                user=self.user,
                image="meva.jpg",
                olingan_price=random.randint(10000, 30000),
                sotuv_price=random.randint(10000, 30000),
                optom_price=random.randint(10000, 30000),
                olchov_usuli="kg",
                soni=10
            )
    
    def test_mahsulot_sotish(self):
        self.client.login(username="test_user", password="my_pass")
        url = reverse("sell_product")
        
        context = {
            "name":"Azizjon",
            "savdo_turi":"qarz",
            "selledproduct_set-TOTAL_FORMS":"7",
            "selledproduct_set-INITIAL_FORMS":"0",
            "selledproduct_set-MIN_NUM_FORMS":"0",
            "selledproduct_set-MAX_NUM_FORMS":"1000",
            "selledproduct_set-0-product":1,
            "selledproduct_set-0-soni":5,
            "selledproduct_set-0-type_of_price":"actual",
            "selledproduct_set-1-product":2,
            "selledproduct_set-1-soni":4,
            "selledproduct_set-1-type_of_price":"actual",
            "selledproduct_set-2-product":3,
            "selledproduct_set-2-soni":6,
            "selledproduct_set-2-type_of_price":"actual",
        }
        
        # Sel Productga request jo'natish
        response = self.client.post(url, context)
        
        # Status kodini tekshirish 
        self.assertEqual(response.status_code, 302)
        
        customer = Customer.objects.get(name="Azizjon")
        self.assertEqual(customer.savdo_turi, "qarz")
        self.assertEqual(SelledProduct.objects.filter(customer=customer).count(), 3)
        
        product1 = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        product3 = Product.objects.get(id=3)
        product4 = Product.objects.get(id=4)
        
        self.assertEqual(product1.soni, 5)
        self.assertEqual(product2.soni, 6)
        self.assertEqual(product3.soni, 4)
        self.assertEqual(product4.soni, 10)
    
        if customer.savdo_turi == "qarz":
            debtcustomer = DebtCustomer.objects.get(customer=customer)
            self.assertEqual(debtcustomer.amount, customer.amount)
            self.assertEqual(debtcustomer.is_payed, False)
        
            debt_url = reverse("debt_customer_list")
            
            context = {
                "debt_id":debtcustomer.id,
                "amount":customer.amount,
            }
            
            response2 = self.client.post(debt_url, context)
            
            self.assertEqual(response2.status_code, 302)
            debtcustomer.refresh_from_db()
            self.assertEqual(debtcustomer.is_payed, True)

class IndexPageTextCase(TestCase):
    def test_page_working(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)