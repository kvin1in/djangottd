from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

MAX_WAIT = 10


class NewVisitorTest(FunctionalTest):
    '''тест нового пользователя'''

    def test_can_start_a_list_for_one_user(self):
        '''тест: можно начать список и получить его позже'''
        # Даша слышала про крутое новое приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел.
        self.assertIn("To-Do lists", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби -
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # Когда она нажимает Enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется и теперь показывает оба элемента ее списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Удовлетворенная, она снова ложится спать

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''тест: многочисленные посетители могут начать списки с разным url'''
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Она замечает, что ее список имеет уникальный url
        daria_list_url = self.browser.current_url
        self.assertRegex(daria_list_url, '/lists/.+')

        # Теперь новый пользователь Франсис, приходит на сайт

        # Мы испозуем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        # информация от Даши не прошла через сеанс
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Френсис посещает домашнюю страницу. Нет никаких признаков Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Френсис начинает новый список, вводя новый элемент. Он менее
        # интересен, чем список Даши....
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Френсис получает уникальный url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotIn(francis_list_url, daria_list_url)

        # Опять-таки, нет следа от списка Даши
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)