from selenium import webdriver
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
        self.fail('Закончить тест!')

        # User enter new list element

        # User enter 'Buy some milk'

        # User press 'Enter'. Page refresh. Now page content line 
        # 'Buy some milk' as new element

        # Text field still able to add anothe element

        # User enter 'Make scrambled eggs'

        # Page refresh. Both elements show.

        # Website generate new unic URL-adress for every user. User see popup 
        # message to explain this behaviour.

        # User browse to this URl. List still there.

        # User quit.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
