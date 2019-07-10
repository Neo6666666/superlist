from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):
    """Home page test"""

    def test_homepage_returns_correct_html(self):
        """Test: Home page returns correct HTML"""
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'lists/home.html')


class ListAndItemModelsTest(TestCase):
    """Listitem model test"""

    def test_saving_and_retrieving_items(self):
        """Тест: Сохранение и получение объектов"""
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        saved_list = List.objects.first()
        first_saved_item = saved_items[0]
        second_saved_items = saved_items[1]

        self.assertEqual(saved_list, list_)
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_items.text, 'Item the second')
        self.assertEqual(second_saved_items.list, list_)


class ListViewTest(TestCase):
    """Тест представления списка"""

    def test_displays_all_items(self):
        """Тест: Отображаются все елементы списка"""
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/new-list')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        """Тест: используется ли шаблон списка."""
        response = self.client.get('/lists/new-list')
        self.assertTemplateUsed(response, 'lists/list.html')


class NewListTest(TestCase):
    """Тест нового списка"""

    def test_can_save_post_request(self):
        """Тест:Мы можем сохранить POST запрос"""
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        """Тест: Перенаправляем после POST запроса"""
        response = self.client.post('/lists/new',
                                    data={'item_text': 'A new list item'})

        self.assertRedirects(response, '/lists/new-list')
