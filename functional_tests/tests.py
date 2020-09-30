from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
		self.browser = webdriver.Firefox(firefox_binary=self.binary)

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		# Alex checks out the to do app homepage
		self.browser.get(self.live_server_url)

		# He notices the title of the page metions to-do
		self.assertIn('To-do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-do', header_text)

		# He is given the option to enter a new to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEquals(inputbox.get_attribute('placeholder'), 'Enter new to-do item')

		# He types "Buy food for my dog"
		inputbox.send_keys('Buy food for my dog')

		# When he hits enter, the page updates, and now it lists
		# "1: Buy food for my dog" as the first item in the list
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy food for my dog')

		# He still has the option to enter another item.
		# He enters "Feed my dog"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Feed my dog')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on his list
		self.wait_for_row_in_list_table('1: Buy food for my dog')
		self.wait_for_row_in_list_table('2: Feed my dog')

		# He wonders whether the site will remember his list. Then he sees
		# that the site has generated a unique URL for him -- there is some
		# explanatory text to that effect.

		# He visits that URL - his to-do list is still there.

		# Satisfied, he goes back to sleep

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Alex starts a new list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy food for my dog')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy food for my dog')

		# He notices that his list has a unique url
		alex_list_url = self.browser.current_url
		self.assertRegex(alex_list_url, '/lists/.+')

		# Now a new user, Monica, comes to the website.
		self.browser.quit()
		self.browser = webdriver.Firefox(firefox_binary=self.binary)

		# Monica visits the home page, there's no sign of Alex's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy food for my dog', page_text)

		# Monica starts a new list by entering a new item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Finish the profession section in Duolingo´s norwegian course')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Finish the profession section in Duolingo´s norwegian course')

		# Monica gets her own unique url
		monica_list_url = self.browser.current_url
		self.assertRegex(monica_list_url, '/lists/.+')
		self.assertNotEqual(monica_list_url, alex_list_url)

		# Satisfied, they both go back to sleep 