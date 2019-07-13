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

    def test_display_only_items_for_that_list(self):
        """Тест: Отображаются все елементы для этого списка"""
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Other itemey 1', list=other_list)
        Item.objects.create(text='Other itemey 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Other itemey 1')
        self.assertNotContains(response, 'Other itemey 2')

    def test_uses_list_template(self):
        """Тест: используется ли шаблон списка."""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        """Тест: Передается правильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)


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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
    """Тест нового элемента списка"""

    def test_can_save_a_post_request_to_existing_list(self):
        """Тест: Можно сохранить POST запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for existing list'}
        )
        new_item = Item.objects.first()

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(new_item.text, 'A new item for existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """Тест: Переадресация в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data = {'item_text': 'A new item for existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
