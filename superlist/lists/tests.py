from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string


class HomePageTest(TestCase):
    """Home page test"""
    
    def test_homepage_returns_correct_html(self):
        "Test: Home page returns correct HTML"
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')