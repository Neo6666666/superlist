from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    '''Тест нового посетителя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''Тест: начинаем список и можем получить его позже'''

        # User open homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(2)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy some milk' for row in rows))

        # Text field still able to add anothe element
        self.fail('Закончить тест!')
        # User enter 'Make scrambled eggs'

        # Page refresh. Both elements show.

        # Website generate new unic URL-adress for every user. User see popup 
        # message to explain this behaviour.

        # User browse to this URl. List still there.

        # User quit.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
