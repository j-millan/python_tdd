from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from lists.views import home
from lists.models import Item

class HomePageTests(TestCase):
	def test_uses_home_template(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'lists/home.html')

	def test_only_saves_items_on_POST_requests(self):
		self.client.get(reverse('home'))
		self.assertEqual(Item.objects.count(), 0)

	def test_can_save_POST_request(self):
		response = self.client.post(reverse('home'), data={'item_text': 'Play Minecraft'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'Play Minecraft')

	def test_redirects_after_POST_request(self):
		response = self.client.post(reverse('home'), data={'item_text': 'Play Minecraft'})
		self.assertRedirects(response, reverse('home'))

	def test_displays_all_list_items(self):
		item1 = Item.objects.create(text='Item 1')
		item2 = Item.objects.create(text='Item 2')

		response = self.client.get(reverse('home'))
		self.assertContains(response, 'Item 1')
		self.assertContains(response, 'Item 2')

class ItemModelTests(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item.objects.create(text='Buy food for my dog.')
		second_item = Item.objects.create(text='Feed my dog.')

		saved_items = Item.objects.all()
		self.assertEquals(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Buy food for my dog.')
		self.assertEqual(second_saved_item.text, 'Feed my dog.')