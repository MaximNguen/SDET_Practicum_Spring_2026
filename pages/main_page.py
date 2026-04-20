from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import allure
from typing import List
import random

from pages.base_page import BasePage
from data.locators_main import MainPageLocators as MPL
from data.mock_data import search_value

class MainPage(BasePage):
    """
    Класс для взаимодействия с главной страницей.
    Содержит методы для работы с элементами страницы.
    """
    
    def __init__(self, driver):
        super().__init__(driver)

    def get_navbar(self):
        with allure.step("Получаем WebElement навигационной панели"):
            nav = self.find_element(*MPL.navbar_list)
            self.scroll(nav)
            return nav
    
    def get_navbar_items(self) -> List[str]:
        """Получить список категорий из навигационной панели."""
        with allure.step("Получаем названия категорий из навигационной панели"):
            category_elements = self._get_category_elements()
            category_names = []
            
            for element in category_elements:
                name = self._clean_category_name(element.text)
                if name:
                    category_names.append(name)
            
            return category_names
    
    def click_category(self, category_name: str) -> None:
        """Клик по категории в навигационной панели."""
        with allure.step(f"Кликаем по категории: {category_name}"):
            category_element = self._find_category_by_name(category_name)
            previous_url = self.driver.current_url
            category_element.click()
            self.wait.wait_until_url_change(previous_url=previous_url)
            self.wait.wait_for_page_load()
            
    def get_search_input(self):
        """Получить элемент поля поиска на главной странице."""
        with allure.step("Получаем элемент поля поиска на главной странице"):
            search_input = self.find_element(*MPL.search_input)
            self.scroll(search_input)
            return search_input

    def get_products_cards(self) -> List[WebElement]:
        """Получить карточки товаров на главной странице."""
        with allure.step("Получаем карточки товаров на главной странице"):
            cards = self.find_elements(*MPL.product_cards)
            valid_cards = []
            for card in cards:
                if card.find_elements(*MPL.product_name):
                    valid_cards.append(card)
            return valid_cards

    def get_product_name_from_card(self, card: WebElement) -> str:
        """Получить название товара из карточки на главной странице."""
        with allure.step("Получаем название товара из карточки"):
            name_element = card.find_element(*MPL.product_name)
            return name_element.text.strip()

    def get_random_product_card(self, excluded_product_names: List[str] = None) -> tuple[WebElement, str]:
        """Получить случайную карточку товара на главной странице."""
        with allure.step("Выбираем случайную карточку товара на главной странице"):
            cards = self.get_products_cards()
            if excluded_product_names is None:
                excluded_product_names = []

            available_cards = []
            for card in cards:
                product_name = self.get_product_name_from_card(card)
                if product_name and product_name not in excluded_product_names:
                    available_cards.append((card, product_name))

            if not available_cards:
                raise ValueError("Недостаточно карточек товаров для случайного выбора.")

            selected_card, selected_name = random.choice(available_cards)
            return selected_card, selected_name

    def get_button_cart(self, card: WebElement) -> WebElement:
        """Получить кнопку добавления товара в корзину на карточке."""
        with allure.step("Получаем кнопку добавления товара в корзину на карточке"):
            button = card.find_element(*MPL.product_cart_button)
            self.scroll(button)
            return button

    def open_product_page_from_card(self, card: WebElement) -> None:
        """Открыть страницу товара по карточке на главной странице."""
        with allure.step("Открываем страницу товара по карточке на главной странице"):
            product_link = card.find_element(*MPL.product_name)
            self.scroll(product_link)
            previous_url = self.driver.current_url
            product_link.click()
            self.wait.wait_until_url_change(previous_url=previous_url)
            self.wait.wait_for_page_load()

    def click_add_cart_button(self, card: WebElement) -> None:
        """Клик по кнопке добавления товара в корзину на главной странице."""
        with allure.step("Кликаем по кнопке добавления товара в корзину на главной странице"):
            button = self.get_button_cart(card)
            previous_url = self.driver.current_url
            button.click()
            self.wait.wait_until_url_change(previous_url=previous_url)
            self.wait.wait_for_page_load()
        
    def enter_search_value(self, element: WebElement) -> None:
        """Ввести значение в поле поиска."""    
        with allure.step(f"Вводим значение '{search_value}' в поле поиска"):
            self.input_text(element, text=search_value)
            self.input_enter(element)
            
    def go_to_cart_page(self):
        """Перейти на страницу корзины."""
        with allure.step("Переходим на страницу корзины"):
            cart_button = self.find_element(*MPL.cart_button)
            self.scroll(cart_button)
            previous_url = self.driver.current_url
            cart_button.click()
            self.wait.wait_until_url_change(previous_url=previous_url)
            self.wait.wait_for_page_load()

    
    def _get_category_elements(self) -> List[WebElement]:
        """
        Получить элементы категорий (приватный метод).
        Возвращает WebElement'ы только для внутреннего использования.
        """
        navbar = self.find_element(*MPL.navbar_list)
        self.scroll(navbar)
        all_li_elements = navbar.find_elements(By.TAG_NAME, 'li')

        category_elements = []
        for element in all_li_elements:
            text = element.text.strip()
            if text and text.upper() != 'HOME':
                category_elements.append(element)
        
        return category_elements

    def _find_category_by_name(self, category_name: str) -> WebElement:
        """
        Найти элемент категории по названию (приватный метод).
        Возвращает WebElement для дальнейших действий.
        """
        category_elements = self._get_category_elements()

        for element in category_elements:
            current_name = self._clean_category_name(element.text)
            if current_name.upper() == category_name.upper():
                return element

        raise ValueError(f"Категория '{category_name}' не найдена в навигационной панели.")

    def _clean_category_name(self, name: str) -> str:
        """Очистить название категории от HTML сущностей и пробелов."""
        if not name:
            return ""
        cleaned = name.strip()
        cleaned = cleaned.replace('&amp;', '&')
        return cleaned