from django.urls import reverse, resolve 
from django.test import TestCase, Client
import random 
import string

class TestCases(TestCase):
    def generate_email(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = ''.join(random.choices(string.ascii_lowercase, k=10))
        tlds = ['com', 'net', 'org', 'edu', 'gov']
        tld = random.choice(tlds)
        email = f"{username}@{domain}.{tld}"
        return email

    def generate_password(self):
        length = random.randint(1, 20)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return password
    
    def setUp(self):
        self.client = Client()
        self.email = self.generate_email()
        self.password = self.generate_password() 

    def Test_signup(self):
        url = reverse('signup')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data)
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mSign up test passed\033[0m")
        except AssertionError:
            print("\033[91mSign up test failed\033[91m")

    def Test_login(self, password, login_test_type='Login'):
        url = reverse('login')
        data = {
            "email": self.email,
            "password": password
        }
        response = self.client.post(url, data)
        try:
            self.assertEqual(response.status_code, 200) 
            print(f"\033[92m{login_test_type} test passed\033[0m")
        except AssertionError: 
            print(f"\033[91m{login_test_type} test failed\033[91m")

    def Test_forgot_password(self):
        url = reverse('forgot_password')
        data = {
            "email": self.email
        }
        response = self.client.post(url, data)
        try: 
            self.assertEqual(response.status_code, 200)
            print("\033[92mForgot password test passed\033[0m")
        except AssertionError:
            print("\033[91mForgot password test failed\033[91m")

    def Test_verify_forgot_password_code(self): 
        url = reverse('verify_forgot_password_code', args=[1234])
        response = self.client.post(url)
        # TODO: complete this when verify forgot password is ready 

    def Test_set_new_password(self):
        url = reverse('set_new_password')
        data = {
            "email": self.email,
            "password": self.generate_password()
        }
        response = self.client.post(url, data)
        try: 
            self.assertEqual(response.status_code, 200)
            print("\033[92mSet new password test passed\033[0m")
        except AssertionError:
            print("\033[91mSet new password test failed\033[91m")

        # Check that it's possible to login with the new password 
        self.Test_login('newpass', login_test_type='Relogin')

    def test_runner(self):
        self.Test_signup()
        self.Test_login(self.password)
        self.Test_forgot_password()
        self.Test_verify_forgot_password_code()
        self.Test_set_new_password()