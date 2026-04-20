from selenium.webdriver.remote.webdriver import WebDriver
import allure

from pages.main_page import MainPage
from pages.items_page import ItemPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

class PageFactory:
    """
    Фабрика для создания и управления страницами.
    Реализует паттерн Factory.
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.pages_data = {
            "main_page": MainPage(self.driver),
            "items_page": ItemPage(self.driver),
            "search_page": SearchPage(self.driver),
            "product_page": ProductPage(self.driver),
            "cart_page": CartPage(self.driver)
        }
        
    def get_page(self, page_name: str) -> object:
        """Получить страницу по имени."""
        if page_name in self.pages_data:
            return self.pages_data[page_name]
        else:
            raise ValueError(f"Страница '{page_name}' не найдена в фабрике.")
    
    @property
    def main_page(self) -> MainPage:
        """Получить главную страницу."""
        return self.get_page("main_page")

    @property
    def items_page(self) -> ItemPage:
        """Получить страницу товаров."""
        return self.get_page("items_page")

    @property
    def search_page(self) -> SearchPage:
        """Получить страницу поиска."""
        return self.get_page("search_page")

    @property
    def product_page(self) -> ProductPage:
        """Получить страницу товара."""
        return self.get_page("product_page")

    @property
    def cart_page(self) -> CartPage:
        """Получить страницу корзины."""
        return self.get_page("cart_page")