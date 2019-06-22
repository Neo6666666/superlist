from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


class HomePageTest(TestCase):
    """Home page test"""

    def test_root_url_resolves_to_home_page_view(self):
        """Test: root url resolves to home page view"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_homepage_returns_correct_html(self):
        "Test: Home page returns correct HTML"
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))