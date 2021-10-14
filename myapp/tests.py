from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Product


User = get_user_model()

class ProductTestCase(TestCase):
    
    def setUp(self):
        user_a = User(username='bruce2', email='bruce2@gmail.com')
        user_pswd = 'us222'
        
        self.user_pswd = user_pswd
        
        user_a.is_staff = True
        user_a.is_superuser = False
        user_a.set_password(user_pswd)
        user_a.save()
        self.user_a = user_a
        
        
        # another user
        user_b = User.objects.create_user('user_2', 'user2@gmail.com', 'user1234')
        self.user_b = user_b 
        
        
    def test_user_count(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)
        
    def test_invalid_request(self): # logged in session
        self.client.login(username=self.user_b.username, password='user1234')
        response = self.client.post(
            '/product/create/',
            {'title': 'Valid test'}
            )

        # self.assertTrue(response.status_code!=200)
        self.assertNotEqual(response.status_code, 200)
        
        
    def test_valid_request(self):
        self.client.login(username=self.user_a.username, password='us222')
        response = self.client.post(
            '/product/create/', 
            {'title': 'valid test'}
            )
        self.assertEqual(response.status_code, 200)        