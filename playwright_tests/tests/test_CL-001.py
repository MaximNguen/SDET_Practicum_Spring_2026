import logging
import random

import pytest
from playwright.sync_api import expect

from playwright_tests.data.expected_data import expected_categories
from playwright_tests.data.urls import main_page_url

logger = logging.getLogger(__name__)


class TestFilterPerformance:
    """Тест-кейсы для проверки производительности фильтра товаров."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(main_page_url)
        yield

    def test_check_products_in_category(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            self.main_page.click_category(category)
            expect(self.main_page.page).not_to_have_url(main_page_url)
            names = self.items_page.get_products_names()
            assert names, f"На странице категории '{category}' не найдено товаров."
            assert len(names) >= 4, (
                f"На странице категории '{category}' найдено меньше 4 товаров."
            )

    def test_check_filter_performance(self):
        category = random.choice(expected_categories)
        self.main_page.click_category(category)
        expect(self.main_page.page).not_to_have_url(main_page_url)
        expect(self.items_page.get_filter_select()).to_be_visible()

    def test_check_filter_sorting_price_asc(self):
        for category in self.main_page.get_navbar_items():
            self.main_page.click_category(category)
            cards = self.items_page.get_product_cards()
            self.items_page.select_filter_option("Price Low > High")
            prices = self.items_page.get_products_prices()
            assert cards.count() > 0, f"На странице категории '{category}' не найдено товаров."
            assert prices == sorted(prices), (
                f"Товары в категории '{category}' не отсортированы по цене от дешевых к дорогим."
            )

    def test_check_filter_sorting_price_desc(self):
        for category in self.main_page.get_navbar_items():
            self.main_page.click_category(category)
            cards = self.items_page.get_product_cards()
            self.items_page.select_filter_option("Price High > Low")
            prices = self.items_page.get_products_prices()
            assert cards.count() > 0, f"На странице категории '{category}' не найдено товаров."
            assert prices == sorted(prices, reverse=True), (
                f"Товары в категории '{category}' не отсортированы по цене от дорогих к дешевым."
            )

    def test_check_filter_sorting_name_asc(self):
        for category in self.main_page.get_navbar_items():
            self.main_page.click_category(category)
            cards = self.items_page.get_product_cards()
            self.items_page.select_filter_option("Name A - Z")
            names = self.items_page.get_products_names()
            assert cards.count() > 0, f"На странице категории '{category}' не найдено товаров."
            assert names == sorted(names), (
                f"Товары в категории '{category}' не отсортированы по названию от A до Z."
            )

    def test_check_filter_sorting_name_desc(self):
        for category in self.main_page.get_navbar_items():
            self.main_page.click_category(category)
            cards = self.items_page.get_product_cards()
            self.items_page.select_filter_option("Name Z - A")
            names = self.items_page.get_products_names()
            assert cards.count() > 0, f"На странице категории '{category}' не найдено товаров."
            assert names == sorted(names, reverse=True), (
                f"Товары в категории '{category}' не отсортированы по названию от Z до A."
            )
