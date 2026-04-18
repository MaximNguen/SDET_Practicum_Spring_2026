import allure
import pytest
import random

from pages.base_page import BasePage
from data.locators_product import ProductPageLocators as PPL

class ProductPage(BasePage):
    """
    Класс для взаимодействия со страницей товара.
    Содержит методы для работы с элементами страницы.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_input_quantity(self):
        """Получить элемент поля ввода количества товара."""
        with allure.step("Получаем элемент поля ввода количества товара"):
            input_quantity = self.find_element(*PPL.input_quantity)
            self.scroll(input_quantity)
            return input_quantity
        
    def set_random_quantity(self, min_value: int = 1, max_value: int = 10) -> None:
        """Установить случайное количество товара в поле ввода."""
        with allure.step(f"Устанавливаем случайное количество товара от {min_value} до {max_value}"):
            random_quantity = random.randint(min_value, max_value)
            self.input_text(self.get_input_quantity(), text=str(random_quantity))
            
    def get_add_to_cart_button(self):
        """Получить элемент кнопки добавления товара в корзину."""
        with allure.step("Получаем элемент кнопки добавления товара в корзину"):
            button = self.find_element(*PPL.add_to_cart_button)
            self.scroll(button)
            return button
        
    def click_add_to_cart_button(self):
        """Клик по кнопке добавления товара в корзину."""
        with allure.step("Кликаем по кнопке добавления товара в корзину"):
            button = self.get_add_to_cart_button()
            button.click()
            self.wait.wait_until_url_change()
            self.wait.wait_for_page_load()
    
    