from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import allure
from typing import List

from pages.base_page import BasePage
from data.locators_main import MainPageLocators as MPL

class MainPage(BasePage):
    """
    Класс для взаимодействия с главной страницей.
    Содержит методы для работы с элементами страницы.
    """
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_navbar_items(self) -> List[str]:
        """Получить список категорий из навигационной панели."""
        with allure.step("Получаем список категорий из навигационной панели"):
            navbar = self.find_element(*MPL.navbar_list)
            category_links = navbar.find_elements(By.TAG_NAME, 'li')
            categories = []
            for link in category_links:
                text = link.text.strip()
                if text and text.upper() != 'HOME':
                    text = text.replace('&amp;', '&')
                    categories.append(link)
            
            return categories
        
    def get_navbar_items_text(self) -> List[str]:
        """Получить список названий категорий из навигационной панели."""
        with allure.step("Получаем названия категорий из навигационной панели"):
            navbar = self.find_element(*MPL.navbar_list)
            category_links = navbar.find_elements(By.TAG_NAME, 'li')
            categories = []
            for link in category_links:
                text = link.text.strip()
                if text and text.upper() != 'HOME':
                    text = text.replace('&amp;', '&')
                    categories.append(text)
            return categories
    
    def click_category(self, category_name: str) -> None:
        """Клик по категории в навигационной панели."""
        with allure.step(f"Кликаем по категории: {category_name}"):
            categories = self.get_navbar_items()
            names = [item.text.strip().upper() for item in categories]
            if category_name.upper() not in names:
                raise ValueError(f"Категория '{category_name}' не найдена в навигационной панели.")
            
            for item in categories:
                if item.text.strip().upper() == category_name.upper():
                    item.click()
                    return 
                
                
    def get_mock_data_category(self) -> str:
        categories = self.get_navbar_items()
        data = {}
        
        for item in categories:
            name = item.text.strip().upper()
            if name and name != 'HOME':
                data["name"] = item
        return data