from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import List
from selenium.webdriver.common.keys import Keys

from data.locators_cart import CartPageLocators as CPL
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Класс для взаимодействия со страницей корзины.
    Содержит методы для работы с элементами страницы.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_table_cart(self) -> WebElement:
        """Получить элемент таблицы корзины."""
        with allure.step("Получаем элемент таблицы корзины"):
            table = self.find_element(*CPL.table)
            self.scroll(table)
            return table
        
    def get_cart_items(self) -> List[WebElement]:
        """Получить элементы строк товаров в корзине."""
        with allure.step("Получаем элементы строк товаров в корзине"):
            table = self.get_table_cart()
            items = table.find_elements(*CPL.cart_rows)
            return items
        
    def get_cart_items_data(self) -> List[dict]:
        """Получить данные о товарах в корзине."""
        with allure.step("Получаем данные о товарах в корзине"):
            items = self.get_cart_items()
            cart_data = []
            for item in items:
                name = item.find_element(*CPL.name_product).text.strip()
                price_element = item.find_element(*CPL.unit_price)
                quantity = item.find_element(*CPL.quantity_input).get_attribute('value')
                self.scroll(price_element)
                price_text = price_element.text.strip().replace('$', '')
                try:
                    price = float(price_text)
                except ValueError:
                    price = None
                cart_data.append({'name': name, 'price': price, 'quantity': quantity})
            return cart_data
    
    def get_total_price(self) -> float:
        """Получить общую стоимость товаров в корзине."""
        with allure.step("Получаем общую стоимость товаров в корзине"):
            total_element = self.find_element(*CPL.total_price)
            self.scroll(total_element)
            total_text = total_element.text.strip().replace('Total: $', '')
            try:
                total_price = float(total_text)
                return total_price
            except ValueError:
                return None
    
    def get_lowest_price_item(self) -> dict:
        """Получить товар с самой низкой ценой в корзине."""
        with allure.step("Получаем товар с самой низкой ценой в корзине"):
            cart_data = self.get_cart_items_data()
            lowest_price_item = min(cart_data, key=lambda x: x['price'] if x['price'] is not None else float('inf'))
            return lowest_price_item
        
    def get_item_input_quantity_lowest_price(self) -> WebElement:
        """Получить элемент поля количества для товара с самой низкой ценой в корзине."""
        with allure.step("Получаем элемент поля количества для товара с самой низкой ценой в корзине"):
            lowest_price_item = self.get_lowest_price_item()
            items = self.get_cart_items()
            for item in items:
                name = item.find_element(*CPL.name_product).text.strip()
                if name == lowest_price_item['name']:
                    quantity_input = item.find_element(*CPL.quantity_input)
                    self.scroll(quantity_input)
                    return quantity_input
            return None
        
    def double_quantity_lowest_price_item(self) -> None:
        """Удвоить количество товара с самой низкой ценой в корзине."""
        with allure.step("Удваиваем количество товара с самой низкой ценой в корзине"):
            quantity_input = self.get_item_input_quantity_lowest_price()
            if quantity_input:
                current_value = quantity_input.get_attribute('value')
                try:
                    current_quantity = int(current_value)
                    new_quantity = current_quantity * 2
                    self.input_text(quantity_input, text=str(new_quantity))
                except ValueError:
                    pass