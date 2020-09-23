from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from lists.views import home

class HomeViewTests(TestCase):
	def test_uses_home_template(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'lists/home.html')

	def test_can_save_POST_request(self):
		response = self.client.post(reverse('home'), data={'item_text': 'Play Minecraft'})
		self.assertContains(response, 'Play Minecraft')
		self.assertTemplateUsed(response, 'lists/home.html')