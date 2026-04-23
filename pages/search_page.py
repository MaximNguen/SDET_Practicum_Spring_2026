from asyncio.log import logger
import logging

from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import List

from pages.base_page import BasePage
from data.ui_data.locators_search import SearchPageLocators as SPL

logger = logging.getLogger(__name__)
    
class SearchPage(BasePage):
    """
    Класс для взаимодействия со страницей поиска.
    Содержит методы для работы с элементами страницы.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def get_products_cards(self) -> List[WebElement]:
        """Получить элементы карточек товаров на странице поиска."""
        with allure.step("Получаем элементы карточек товаров на странице поиска"):
            logger.info("Получаем элементы карточек товаров на странице поиска")
            cards = self.find_elements(*SPL.cards)
            return cards

    def get_products_current_items(self, numbers: List[int]) -> List[WebElement]:
        """Получить нужные карточки товаров на странице поиска."""
        with allure.step("Получаем нужные карточки товаров на странице поиска"):
            logger.info("Получаем нужные карточки товаров на странице поиска")
            cards = self.get_products_cards()
            current_cards = []
            for i, card in enumerate(cards):
                if i + 1 not in numbers:
                    continue
                current_cards.append(card)
            return current_cards

    def get_button_cart(self, element: WebElement) -> WebElement:
        """Получить элемент кнопки добавления товара в корзину на странице поиска."""
        with allure.step(
            "Получаем элемент кнопки добавления товара в корзину на странице поиска"
        ):
            logger.info("Получаем элемент кнопки добавления товара в корзину на странице поиска")
            button = element.find_element(*SPL.cart_button)
            self.scroll(button)
            return button

    def click_add_cart_button(self, card: WebElement) -> None:
        """Клик по кнопке добавления товара в корзину."""
        with allure.step("Кликаем по кнопке добавления товара в корзину"):
            logger.info("Кликаем по кнопке добавления товара в корзину")
            button = self.get_button_cart(card)
            self.scroll(button)
            previous_url = self.get_current_url()
            button.click()
            self.wait.wait_until_url_change(previous_url=previous_url)
            self.wait.wait_for_page_load()
