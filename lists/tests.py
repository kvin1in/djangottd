from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    '''тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        '''тест сохранения и получения элементов списка'''
        first_item = Item()
        first_item.text = 'This first (even) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'This first (even) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class HomePageTest(TestCase):
    '''Тестирование стартовой страницы'''

    def test_uses_home_template(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_returns_correct_html(self):
        '''тест: домашняя страница возвращает правильный html'''
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))

        self.assertTemplateUsed(response, 'home.html')


class LiveTestView(TestCase):
    '''тест представления списка'''

    def test_can_save_a_POST_request_to_an_existing_list(self):
        '''тест можно сохранить как post-запрос'''
        order_list = List.objects.create()
        corrent_list = List.objects.create()

        response = self.client.post(
            f'/lists/{corrent_list.id}/add_item',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, corrent_list)

    def test_redirects_to_list_view(self):
        '''тест: переадресует в представление списка'''
        order_list = List.objects.create()
        corrent_list = List.objects.create()

        response = self.client.post(
            f'/lists/{corrent_list.id}/add_item',
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(response, f'/lists/{corrent_list.id}/')

    def test_can_save_a_POST_request(self):
        '''тест можно сохранить как post-запрос'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, f'/lists/1/')
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''тест: переадресует после post-запроса'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/lists/{new_list.id}/')

    def test_uses_list_template(self):
        '''тест: используется ли правильный шаблон'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_corrent_list_to_template(self):
        '''тест: передается правильный шаблон списка'''
        order_list = List.objects.create()
        corrent_list = List.objects.create()
        response = self.client.get(f'/lists/{corrent_list.id}/')
        self.assertEqual(response.context['list'], corrent_list)

    def test_displays_only_items_for_that_list(self):
        '''тест: отображаются все элементы списка'''
        corrent_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=corrent_list)
        Item.objects.create(text='itemey 2', list=corrent_list)

        response = self.client.get(f'/lists/{corrent_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'Другой элемент 1 списка')
        self.assertNotContains(response, 'Другой элемент 2 списка')
