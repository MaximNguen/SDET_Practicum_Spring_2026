from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
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
            self.scroll(select)
            return select

    def select_filter_option(self, option_text: str) -> None:
        """Выбрать опцию из выпадающего списка для сортировки товаров."""
        with allure.step(
            f"Выбираем опцию '{option_text}' из выпадающего списка для сортировки товаров"
        ):
            select_element = self.get_filter_select()
            select = Select(select_element)
            select.select_by_visible_text(option_text)

    def get_products_cards(self) -> List[WebElement]:
        """Получить элементы карточек товаров на странице."""
        with allure.step("Получаем элементы карточек товаров на странице"):
            cards = self.find_elements(*IPL.cards)
            return cards

    def get_products_prices(self) -> List[float]:
        """Получить цены товаров на странице."""
        with allure.step("Получаем цены товаров на странице"):
            cards = self.get_products_cards()
            prices = []
            for card in cards:
                try:
                    price_element = card.find_element(*IPL.price_product)
                    self.scroll(price_element)
                except:
                    price_element = card.find_element(*IPL.price_product_new)
                    self.scroll(price_element)
                price_text = self.get_text_from_element(price_element).replace("$", "")
                try:
                    price = float(price_text)
                    prices.append(price)
                except ValueError:
                    continue
            return prices

    def get_products_names(self) -> List[str]:
        """Получить названия товаров на странице."""
        with allure.step("Получаем названия товаров на странице"):
            cards = self.get_products_cards()
            names = []
            for card in cards:
                name_text = self.get_text_from_child(card, *IPL.name_product)
                if name_text:
                    names.append(name_text)
            return names
