from django.test import TestCase
from kc.users.models import CustomUser
from faker import Faker
from rest_framework.test import APITestCase, force_authenticate





class AddCategoryAfterCheckoutTestCase(APITestCase):
  

    def test_login(self):
        
        user = CustomUser.objects.create_user(email='test@email.com', password='123123123')
        user.save()
        self.assertEqual(user.email, 'test@email.com')        
        response = self.client.post('auth/token/', {
           'email': user.email,
           'password': user.password
        },
        formet='json'
        )
       
        # self.assertIsNotNone(result.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)

       


    def test_user_checkout(self):
        user = CustomUser.objects.create_user(email='test123@email.com', password='123123123')
       

       
        result = self.client.post('api/v1/checkout/', {
           
            'temp_cat': 8,
            'checkout': 'Zrty4564fdhfddh3lkks34',
            'mail_list': True
        },
        format='json'
        )
       
        self.assertEqual(result.status_code, 202)

        user.tearDown()


