import allure
import pytest
import random

from data.urls import main_page_url
from data.expected_data import expected_categories

@allure.epic("Проверка производительности фильтра товаров")
@allure.feature("Тест-кейсы для проверки производительности фильтра товаров")
class TestFilterPerformance:
    """Тест-кейсы для проверки производительности фильтра товаров."""

    @classmethod
    def setup_class(cls):
        print("\n========= Начало выполнения тест-кейсов на производительность фильтра товаров ==========")

    @classmethod
    def teardown_class(cls):
        print("\n========= Конец выполнения тест-кейсов на производительность фильтра товаров ==========")

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page, url=main_page_url):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()
        
    @allure.story("Проверка наличия товаров всех категориях и количество товаров не меньше 4")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_products_in_category(self):
        """Проверка наличия товаров в каждой категории и количество товаров не меньше 4."""
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем наличие товаров в категории: {category}"):
                self.main_page.click_category(category)
                current_url = self.main_page.driver.current_url
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                products_data = self.items_page.get_products_names()
                assert products_data, f"На странице категории '{category}' не найдено товаров."
                assert len(products_data) >= 4, f"На странице категории '{category}' найдено меньше 4 товаров."
                
    @allure.story("Проверка кликабельности сортировки товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_filter_performance(self):
        """Проверка кликабельности сортировки товаров."""
        category = random.choice(expected_categories)
        with allure.step("Переходим на страницу 1 из категорий"):
            self.main_page.click_category(category)
            current_url = self.main_page.driver.current_url
            assert current_url != main_page_url, \
                f"Клик по категории '{category}' не привел к переходу"
        with allure.step(f"Проверяем наличие сортировку товаров в категории: {category}"):
            select = self.items_page.get_filter_select()
            assert select.is_displayed(), f"Фильтр не отображается на сайте"
            
    @allure.story("Проверка сортировки товаров по цене от дешевых к дорогим")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_filter_sorting_price_asc(self):
        """Проверка сортировки товаров по цене от дешевых к дорогим."""
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Price Low > High")
                products_data = self.items_page.get_products_prices()
                current_url = self.main_page.driver.current_url
                
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(products_data), f"Товары в категории '{category}' не отсортированы по цене от дешевых к дорогим."
                
                self.main_page.open(main_page_url)
                
    @allure.story("Проверка сортировки товаров по цене от дорогих к дешевым")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_filter_sorting_price_desc(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Price High > Low")
                products_data = self.items_page.get_products_prices()
                current_url = self.main_page.driver.current_url
                
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(products_data, reverse=True), f"Товары в категории '{category}' не отсортированы по цене от дорогих к дешевым."
                
                self.main_page.open(main_page_url)
                
    @allure.story("Проверка сортировки товаров по названию от A до Z")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_filter_sorting_name_asc(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Name A - Z")
                products_data = self.items_page.get_products_names()
                current_url = self.main_page.driver.current_url
                
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(products_data), f"Товары в категории '{category}' не отсортированы по названию от A до Z."
                
                self.main_page.open(main_page_url)
                
    @allure.story("Проверка сортировки товаров по названию от Z до A")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_filter_sorting_name_desc(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Name Z - A")
                products_data = self.items_page.get_products_names()
                current_url = self.main_page.driver.current_url
                
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(products_data, reverse=True), f"Товары в категории '{category}' не отсортированы по названию от Z до A."
                self.main_page.open(main_page_url)