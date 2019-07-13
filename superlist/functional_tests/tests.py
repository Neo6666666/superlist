import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидаем строку в таблице скписка"""
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

    def test_layout_and_styling(self):
        """Тест макета и стилевого оформления"""
        # User open home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User see neat centered text area
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # User start new list. Input box still centered.
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_start_a_list_for_one_user(self):
        """Тест: Можно начать список для одного пользователя"""
        # User open homepage
        self.browser.get(self.live_server_url)

        # Title say to user that it To-Do list webpage
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User enter new list element
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User enter 'Buy some milk'
        inputbox.send_keys('Buy some milk')

        # User press 'Enter'. Page refresh. Now page content line
        # 'Buy some milk' as new element
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy some milk')

        # Text field still able to add anothe element
        inputbox = self.browser.find_element_by_id('id_new_item')

        # User enter 'Make scrambled eggs'
        inputbox.send_keys('Make scrambled eggs')
        inputbox.send_keys(Keys.ENTER)

        # Page refresh. Both elements show.
        self.wait_for_row_in_list_table('1: Buy some milk')
        self.wait_for_row_in_list_table('2: Make scrambled eggs')

        # User browse to this URL. List still there.

        # User quit.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: Многочисленные пользователи могут начать списки по
         разным URL"""
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy some milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some milk')

        # Website generate new unic URL-adress for every user. User see popup
        # message to explain this behaviour.
        user_1_list_url = self.browser.current_url
        self.assertRegex(user_1_list_url, '/lists/.+')

        # Now new user enter the main page

        # - We use new browser seans. To make shure what not cookies nor
        # - anything will not bother us.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # New user enter the main page. No signs of other users.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy some milk', page_text)
        self.assertNotIn('Make scrambled eggs', page_text)

        # new user start new list. Enter new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Order pizza')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Order pizza')

        # New user get a unique URL
        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, '/lists/.+')
        self.assertNotEqual(user_1_list_url, user_2_list_url)

        # Still no signs of other users
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy some milk', page_text)
        self.assertIn('Order pizza', page_text)

        # User quit
        self.browser.quit()

if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    pass
