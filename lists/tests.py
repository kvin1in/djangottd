from django.test import TestCase
from django.urls import resolve
from .views import home_page

class HomePageTest(TestCase):
    '''Тестирование стартовой страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''тест: корневой url преобразуется в представление
        страницы'''
        found = resolve('/')
        self.assertEqual(found.func, home_page)