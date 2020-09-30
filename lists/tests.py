from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpRequest
from lists.views import home
from lists.models import List, Item

class HomePageTests(TestCase):
	def test_uses_home_template(self):
		response = self.client.get(reverse('home'))
		self.assertTemplateUsed(response, 'lists/home.html')

class ListViewTests(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_displays_all_items(self):
		list_ = List.objects.create()
		item1 = Item.objects.create(text='Item 1', list=list_)
		item2 = Item.objects.create(text='Item 2', list=list_)

		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertContains(response, 'Item 1')
		self.assertContains(response, 'Item 2')

class NewListTests(TestCase):
	def can_save_POST_request(self):
		response = self.client.post(reverse('new_list'), data={'item_text': 'My new item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item, 'My new item')

	def test_redirects_after_POST_request(self):
		response = self.client.post(reverse('new_list'), data={'item_text': 'My new item'})
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class ListAndItemModelTests(TestCase):
	def test_saving_and_retrieving_items(self):
		list_ = List.objects.create()

		first_item = Item.objects.create(text='Buy food for my dog.', list=list_)
		second_item = Item.objects.create(text='Feed my dog.',list=list_)

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEquals(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Buy food for my dog.')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Feed my dog.')
		self.assertEqual(second_saved_item.list, list_)