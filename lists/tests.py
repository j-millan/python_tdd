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
		response = self.client.get(f'/lists/{List.objects.create().pk}/')
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_passes_correct_list_to_template(self):
		list_ = List.objects.create()
		other_list = List.objects.create()
		response = self.client.get(reverse('list_view', kwargs={'pk': list_.pk}))

		context_list = response.context['list']
		self.assertEqual(context_list, list_)

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='Item 1', list=correct_list)
		Item.objects.create(text='Item 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='Other list item 1', list=other_list)
		Item.objects.create(text='Other list item 2', list=other_list)

		response = self.client.get(reverse('list_view', kwargs={'pk': correct_list.pk}))
		self.assertContains(response, 'Item 1')
		self.assertContains(response, 'Item 2')
		self.assertNotContains(response, 'Other list item 1')
		self.assertNotContains(response, 'Other list item 2')

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

class NewListTests(TestCase):
	def can_save_POST_request(self):
		response = self.client.post(reverse('new_list'), data={'item_text': 'My new item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item, 'My new item')

	def test_redirects_after_POST_request(self):
		response = self.client.post(reverse('new_list'), data={'item_text': 'My new item'})
		list_ = List.objects.first()
		self.assertRedirects(response, reverse('list_view', kwargs={'pk': list_.pk}))

class NewItemTests(TestCase):
	def can_save_a_POST_request_to_an_existing_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		self.client.post(
			reverse('new_item', kwargs={'pk': correct_list.ok}), 
			data={'item_text': 'item for list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.list, correct_list)
		self.assertEqual(new_item.text, 'item for list')

	def test_redirects_to_list_view(self):
		list_ = List.objects.create()

		response = self.client.post(
			reverse('new_item', kwargs={'pk': list_.pk}), 
			data={'item_text': 'item for list'}
		)

		self.assertRedirects(response, reverse('list_view', kwargs={'pk': list_.pk}))