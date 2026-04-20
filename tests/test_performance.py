import allure
import pytest
import random

from data.urls import main_page_url
from data.expected_data import expected_categories
from data.mock_data import random_category

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
    def setup(self, main_page, items_page, url=main_page_url):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()

    @allure.story("Проверка наличия навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_navbar(self):
        nav = self.main_page.get_navbar()
        assert nav.is_displayed(), "Не отображается панель навигационная"
        
    @allure.story("Проверка наличия поля ввода поиска на главной странице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_search_input(self):
        search_input = self.main_page.get_search_input()
        assert search_input.is_displayed(), "Не отображается поле ввода поиска на главной странице"

    @allure.story("Проверка наличия фильтра товаров")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_filter(self):
        """Проверка наличия фильтра товаров."""
        category = random.choice(random_category)
        with allure.step("Переходим на страницу 1 из категорий"):
            self.main_page.click_category(category)

        with allure.step("Проверяем наличие фильтра"):
            filter = self.items_page.get_filter_select()
            assert filter.is_displayed(), "Фильтр не отображается на сайте"
        
    @allure.story("Проверка наличия категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navbar_categories(self):
        """Проверка наличия категорий в навигационной панели."""
        categories = self.main_page.get_navbar_items()
        
        for category in expected_categories:
            with allure.step(f"Проверяем наличие категории: {category}"):
                assert category.upper() in categories, f"Категория '{category}' не найдена в навигационной панели."
                
    @allure.story("Проверка кликабельности категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_random_category(self):
        """Проверка кликабельности категорий в навигационной панели."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем кликабельность категории: {category}"):
            self.main_page.click_category(category)
            current_url = self.main_page.driver.current_url
            assert current_url != main_page_url, \
                f"Клик по категории '{category}' не привел к переходу"
                    
    @allure.story("Проверка кликабельности всех категорий")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_click_all_categories(self):
        """Проверка кликабельности каждой категории в навигационной панели."""
        categories = self.main_page.get_navbar_items()
        
        for category in categories:
            with allure.step(f"Кликаем и проверяем категорию: {category}"):
                self.main_page.click_category(category)
                
                current_url = self.main_page.driver.current_url
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                
                self.main_page.open(main_page_url)
                
    @allure.story("Проверка наличия товаров на странице категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_category_products(self):
        """Проверка наличия товаров на странице категории."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем наличие товаров в категории: {category}"):
            self.main_page.click_category(category)
            products_data = self.items_page.get_products_cards()
            assert products_data, f"На странице категории '{category}' не найдено товаров."
            
    @allure.story("Проверка кликабельности сортировки товаров")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sorting_products(self):
        """Проверка кликабельности сортировки товаров."""
        category = random.choice(random_category)
        with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
            self.main_page.click_category(category)
            self.items_page.select_filter_option("Price Low > High")
            products_data = self.items_page.get_products_prices()
            assert products_data, f"На странице категории '{category}' не найдено товаров."
