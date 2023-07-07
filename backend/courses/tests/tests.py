from django.urls import reverse, resolve 
from django.test import TestCase, Client
import random 
import string

class TestCases(TestCase):
    def setUp(self):
        self.client = Client()
        pass

    def test_runner(self):
        pass