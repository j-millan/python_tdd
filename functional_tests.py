from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
		self.browser = webdriver.Firefox(firefox_binary=binary)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# A guy checks out the to do app homepage
		self.browser.get('http://127.0.0.1:8000/')

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
		time.sleep(3)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy food for my dog', [row.text for row in rows])

		# He still has the option to enter another item.
		# He enters "Feed my dog"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Feed my dog')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(3)

		# The page updates again, and now shows both items on his list
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy food for my dog', [row.text for row in rows])
		self.assertIn('2: Feed my dog', [row.text for row in rows])

		self.fail('Finish the test!')


		# He wonders whether the site will remember his list. Then he sees
		# that the site has generated a unique URL for him -- there is some
		# explanatory text to that effect.

		# He visits that URL - his to-do list is still there.

		# Satisfied, he goes back to sleep

if __name__ == '__main__':  
	unittest.main(warnings='ignore')