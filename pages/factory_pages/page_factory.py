from selenium.webdriver.remote.webdriver import WebDriver
import allure


class PageFactory:
    """
    Фабрика для создания и управления страницами.
    Реализует паттерн Factory.
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.main_page = None
        self.items_page = None
    
    def get_main_page(self, refresh: bool = False) -> object:
        """Получить экземпляр главной страницы."""
        if refresh or self.main_page is None:
            with allure.step("Создаем экземпляр главной страницы"):
                from pages.main_page import MainPage
                self.main_page = MainPage(self.driver)
        
        return self.main_page
    
    def get_items_page(self, refresh: bool = False) -> object:
        """Получить экземпляр страницы товаров."""
        if refresh or self.items_page is None:
            with allure.step("Создаем экземпляр страницы товаров"):
                from pages.items_page import ItemPage
                self.items_page = ItemPage(self.driver)
        
        return self.items_page
    
    def reset(self):
        """Сбросить состояние страницы (очистить кэш)."""
        with allure.step("Сбрасываем состояние страницы"):
            self.main_page = None
            self.items_page = None