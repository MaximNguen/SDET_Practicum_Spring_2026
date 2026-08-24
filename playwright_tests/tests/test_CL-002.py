import logging

import pytest
from playwright.sync_api import expect

from playwright_tests.data.urls import main_page_url

logger = logging.getLogger(__name__)


class TestSearchAndCartFunctionality:
    """Тест-кейсы для проверки добавления товара в корзину, поиск и изменение корзины."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, product_page, cart_page, search_page):
        self.main_page = main_page
        self.product_page = product_page
        self.cart_page = cart_page
        self.search_page = search_page
        self.main_page.open(main_page_url)
        yield

    def _add_product_to_cart_from_search(self, position: int) -> None:
        search_input = self.main_page.get_search_input()
        self.main_page.enter_search_value(search_input)
        cards = self.search_page.get_products_current_items([position])
        assert len(cards) == 1, (
            f"Не найдена карточка товара с позицией {position}."
        )
        self.search_page.click_add_cart_button(cards[0])
        expect(self.product_page.get_input_quantity()).to_be_visible()
        self.product_page.set_random_quantity()
        self.product_page.click_add_to_cart_button()

    def test_check_search_input(self):
        expect(self.main_page.get_search_input()).to_be_visible()

    def test_check_search_results(self):
        search_input = self.main_page.get_search_input()
        self.main_page.enter_search_value(search_input)
        expect(self.search_page.get_products_cards()).not_to_have_count(0)

    def test_check_add_to_cart_button(self):
        for position in [2, 3]:
            self._add_product_to_cart_from_search(position)
            self.main_page.open(main_page_url)
        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, "В корзине не найдено товаров после добавления."

    def test_change_quantity_for_lowest(self):
        for position in [2, 3]:
            self._add_product_to_cart_from_search(position)
            self.main_page.open(main_page_url)
        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, "В корзине не найдено товаров после добавления."

        total_price = self.cart_page.get_total_price()
        assert total_price > 0, "Общая стоимость корзины не отображается или равна нулю."

        lowest = self.cart_page.get_lowest_price_item()
        self.cart_page.double_quantity_lowest_price_item()
        new_total_price = self.cart_page.get_total_price()

        delta = lowest["quantity"] * lowest["price"]
        assert new_total_price == pytest.approx(total_price + delta, abs=0.01), (
            "Общая стоимость корзины не изменилась на сумму удвоенного количества."
        )
