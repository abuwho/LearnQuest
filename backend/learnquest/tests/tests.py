from django.urls import reverse, resolve 
from django.test import TestCase, Client
import random 
import string

from django.db import models
from authentication.models import * 
from django.contrib.auth import get_user_model

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


    def generate_random_text(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_text = ''.join(random.choice(characters) for i in range(length))
        return random_text
    
    def setUp(self):
        self.User = get_user_model()
        self.client = Client()
        self.email = self.generate_email()
        self.password = self.generate_password() 

    def User_signup(self):
        url = reverse('signup')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data)
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mUser signup successful\033[0m")
        except AssertionError:
            print("\033[91mUser signup failed\033[91m")

    def User_login(self):
        url = reverse('login')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data)
        try:
            self.assertEqual(response.status_code, 200) 
            self.token = response.data['token']
            print(f"\033[92mUser login passed\033[0m")
        except AssertionError: 
            print(f"\033[91mUser login failed\033[91m")

    def Test_apply(self):
        self.User_signup()
        self.User_login()

        url = reverse('submit-instructor-application')
        data = {
            "reason": self.generate_random_text(20)
        }
        response = self.client.post(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mApplication submission successful\033[0m")
        except AssertionError:
            print("\033[91mApplication submission failed\033[91m")

    def test_runner(self):
        self.Test_apply()