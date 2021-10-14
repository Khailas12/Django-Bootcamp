from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings    # this is imported for testing the LOGIN_URL assigned in there


User = get_user_model()

# TDD

class UserTestCase(TestCase):
    def setUp(self):    # python's builtin unittest
        user_a = User(username='brucewayne', email='brucewayne123@gmail.com')
        user_a_pswd = 'some_password'
        
        self.user_a_pswd = user_a_pswd
        
        # similar to User.objects.create() or create_user()
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password(user_a_pswd)
        user_a.save()
        self.user_a = user_a
        print(user_a.id)
        
    # the func name should begin with test and the rest can be anything after first underscore
    def test_user_exists(self): 
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1) # asset user_count == 1
        self.assertNotEqual(user_count, 0)  # !=
        
        
    # def test_user_password(self):
    #     # user_queryset = User.objects.filter(username__iexact='brucewayne')
    #     # user_exists = user_queryset.exists() and user_queryset.count() == 1
    #     # self.assertTrue(user_exists)    # true/false
        
    #     # user_a = user_queryset.first()
    #     self.assertTrue(self.user_a.check_password(self.user_a_pswd))   # checking password
        
    def test_user_password(self):
        user_a = User.objects.get(username='brucewayne')
        self.assertEqual(
            user_a.check_password(self.user_a_pswd)
        )
    
    
    def test_login_url(self):
        # login_url = '/login'
        # self.assertEqual(settings.LOGIN_URL, login_url)
        login_url = settings.LOGIN_URL
        
        # python requests -> self.client.get , post
        # response = self.client.post(login_url, {}, follow=True)
        data = {
            'username': 'brucewayne',
            'password': self.user_a_pswd
        }
        response = self.client.post(login_url, data, follow=True)
        # print(dir(response))
        print(response.request)
        status_code = response.status_code
        redirect_path = response.request.get('PATH_INFO')
        
        # self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(status_code, 200)