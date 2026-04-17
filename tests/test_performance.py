import allure
import pytest
import random

from data.urls import main_page_url
from data.expected_data import expected_categories
from data.mock_data import random_category
from pages.items_page import ItemPage

@allure.epic("UI Тесты")
@allure.feature("Тест-кейсы на наличие элементов и их работоспособность")
class TestPositiveResult:
    """Позитивные тест-кейсы для проверки работоспособности элементов сайта."""

    @classmethod
    def setup_class(cls):
        print("\n========= Начало выполнения тест-кейсов на наличие элементов ==========")

    @classmethod
    def teardown_class(cls):
        print("\n========= Конец выполнения тест-кейсов на наличие элементов ==========")

    @pytest.fixture(autouse=True)
    def setup(self, main_page, url=main_page_url):
        self.main_page = main_page
        self.main_page.open(url)
        yield self.main_page
        
    @allure.story("Проверка наличия категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navbar_categories(self):
        """Проверка наличия категорий в навигационной панели."""
        categories = self.main_page.get_navbar_items()
        name_category = [item.text.strip().upper() for item in categories]
        
        for category in expected_categories:
            with allure.step(f"Проверяем наличие категории: {category}"):
                print("Категории на странице:", name_category)
                assert category.upper() in name_category, f"Категория '{category}' не найдена в навигационной панели."
                
    @allure.story("Проверка кликабельности категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_category(self):
        """Проверка кликабельности категорий в навигационной панели."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем кликабельность категории: {category}"):
            for item in self.main_page.get_navbar_items():
                if item.text.strip() == category and item.text.strip() != 'HOME':
                    self.main_page.click_category(category)
                    assert self.main_page.driver.current_url != main_page_url, f"Клик по категории '{category}' не привел к переходу на другую страницу."
                    
    @allure.story("Проверка кликабельности всех категорий")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_categories(self):
        """Проверка кликабельности каждой категории в навигационной панели."""
        categories = self.main_page.get_navbar_items_text()
        
        for category in categories:
            with allure.step(f"Кликаем и проверяем категорию: {category}"):
                self.main_page.click_category(category)
                
                current_url = self.main_page.driver.current_url
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                
                self.main_page.open(main_page_url)
                
    @allure.story("Проверка наличия товаров на странице категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_category_products(self, items_page):
        """Проверка наличия товаров на странице категории."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем наличие товаров в категории: {category}"):
            self.main_page.click_category(category)
            products_data = items_page.get_products_data()
            assert products_data, f"На странице категории '{category}' не найдено товаров."
            
    @allure.story("Проверка кликабельности сортировки товаров")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sorting_products(self, items_page):
        """Проверка кликабельности сортировки товаров."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
            self.main_page.click_category(category)
            items_page.select_filter_option("Price Low > High")
            products_data = items_page.get_products_data()
            prices = [float(price.replace('$', '')) for price in products_data.values()]
            assert prices == sorted(prices), "Товары не отсортированы по цене."