from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import allure
from typing import List

from pages.base_page import BasePage
from data.locators_items import ItemPageLocators as IPL

class ItemPage(BasePage):
    """
    Класс для взаимодействия со страницей товаров.
    Содержит методы для работы с элементами страницы.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def get_filter_select(self):
        """Получить элемент выпадающего списка для сортировки товаров."""
        with allure.step("Получаем элемент выпадающего списка для сортировки товаров"):
            select = self.find_element(*IPL.filter_select)
            return select
        
    def select_filter_option(self, option_text: str) -> None:
        """Выбрать опцию из выпадающего списка для сортировки товаров."""
        with allure.step(f"Выбираем опцию '{option_text}' из выпадающего списка для сортировки товаров"):
            select_element = self.get_filter_select()
            select = Select(select_element)
            select.select_by_visible_text(option_text)
            
    def get_products_data(self) -> dict:
        """Получить данные о товарах на странице."""
        with allure.step("Получаем данные о товарах на странице"):
            products_cards = self.find_elements(*IPL.cards)
            products_dict = {}
            
            for card in products_cards:
                product_name = card.find_element(*IPL.name_product).text.strip()
                try:
                    product_price = card.find_element(*IPL.price_product).text.strip()
                except:
                    try:
                        product_price = card.find_element(*IPL.price_product_new).text.strip()
                    except:
                        continue
                products_dict[product_name] = product_price
                
            if not products_dict:
                raise ValueError("Не удалось найти данные о товарах на странице.")
            return products_dict