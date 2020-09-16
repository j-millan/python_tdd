from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from lists.views import home

class HomeViewTests(TestCase):
	def test_view_function(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_page_returns_correct_html(self):
		request = HttpRequest()
		response = home(request)
		html = response.content.decode()
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-do list</title>', html)
		self.assertTrue(html.endswith('</html>'))