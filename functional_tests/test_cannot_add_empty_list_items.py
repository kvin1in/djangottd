from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Он нажимает на Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке
        # которое говорит, что элементы списка не должны быть пустыми
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Нельзя добавлять пустой лист"
        ))

        # Она пробует снова, теперь с неким текстом для элемента, и теперь
        # это срабатывает
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Как ни странно, Эдит решает оправить элемент второй пустой элемент списка
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # Она получает аналогичную ошибку
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "Нельзя добавлять пустой лист"
        ))

        # И она может его исправить, заполнив поле неким текстом
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')




