import logging
import random

import pytest
from playwright.sync_api import expect

from playwright_tests.data.expected_data import expected_categories
from playwright_tests.data.mock_data import random_category
from playwright_tests.data.urls import main_page_url

logger = logging.getLogger(__name__)


class TestPositiveResult:
    """Позитивные тест-кейсы для проверки работоспособности элементов сайта."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(main_page_url)
        yield

    def test_get_navbar(self):
        expect(self.main_page.get_navbar()).to_be_visible()

    def test_get_search_input(self):
        expect(self.main_page.get_search_input()).to_be_visible()

    def test_get_filter(self):
        category = random.choice(random_category)
        self.main_page.click_category(category)
        expect(self.items_page.get_filter_select()).to_be_visible()

    def test_navbar_categories(self):
        categories = self.main_page.get_navbar_items()
        categories_upper = {c.upper() for c in categories}
        for category in expected_categories:
            assert category.upper() in categories_upper, (
                f"Категория '{category}' не найдена в навигационной панели."
            )

    def test_click_random_category(self):
        category = random.choice(random_category)
        self.main_page.click_category(category)
        expect(self.main_page.page).not_to_have_url(main_page_url)

    def test_click_all_categories(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            self.main_page.click_category(category)
            expect(self.main_page.page).not_to_have_url(main_page_url)
            self.main_page.open(main_page_url)

    def test_category_products(self):
        category = random.choice(random_category)
        self.main_page.click_category(category)
        expect(self.items_page.get_product_cards()).not_to_have_count(0)

    def test_sorting_products(self):
        category = random.choice(random_category)
        self.main_page.click_category(category)
        self.items_page.select_filter_option("Price Low > High")
        prices = self.items_page.get_products_prices()
        assert prices, f"На странице категории '{category}' не найдено товаров."
