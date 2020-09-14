from django.test import TestCase
from django.urls import resolve
from lists.views import home

class HomeViewTests(TestCase):
	def test_view_function(self):
		view = resolve('/')
		self.assertEquals(view.func, home)