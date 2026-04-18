from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import allure
from typing import List

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
            category_element.click()
            self.wait.wait_until_url_change()
            
    def get_search_input(self):
        """Получить элемент поля поиска на главной странице."""
        with allure.step("Получаем элемент поля поиска на главной странице"):
            search_input = self.find_element(*MPL.search_input)
            self.scroll(search_input)
            return search_input
        
    def enter_search_value(self, element: WebElement) -> None:
        """Ввести значение в поле поиска."""    
        with allure.step(f"Вводим значение '{search_value}' в поле поиска"):
            self.input_text(element, text=search_value)
            
    def go_to_cart_page(self):
        """Перейти на страницу корзины."""
        with allure.step("Переходим на страницу корзины"):
            cart_button = self.find_element(*MPL.cart_button)
            self.scroll(cart_button)
            cart_button.click()
            self.wait.wait_until_url_change()
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