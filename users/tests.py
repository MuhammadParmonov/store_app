from django.test import TestCase
from .models import User
from django.contrib.auth import authenticate
# Create your tests here.

class UserModelTestCase(TestCase):
    
    def test_user_auth(self):
        user = User.objects.create(
            username="muhammadali", 
            first_name="Abubakir", 
            last_name="Shokirov",
			email="abu@gmail.com",
			phone_number="+998916781118",
			profile = "profile_images/muhammadali.png",
        )
        
        user.set_password("lionitmesniy")
        user.save()
        #User moduli to'g'ri yaratilganini tekshirildi
        test_user = User.objects.get(username="muhammadali")
        self.assertEqual(test_user.first_name, "Abubakir")
        self.assertEqual(test_user.last_name, "Shokirov")
        self.assertEqual(test_user.email, "abu@gmail.com")
        self.assertEqual(test_user.phone_number, "+998916781118")
        self.assertEqual(test_user.profile, "profile_images/muhammadali.png")
        #Parolni to'g'ri kiritishni tekshirdik
        self.assertTrue(authenticate(username="muhammadali", password="lionitmesniy"))
        self.assertEqual(None, authenticate(username="muhammadali", password="passwor012008"))
        self.assertNotEqual("muhammadali01", test_user.password)
        
    