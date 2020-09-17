from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from lists.views import home

class HomeViewTests(TestCase):
	def test_page_returns_correct_html(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'lists/home.html')