import logging

import pytest
from playwright.sync_api import expect

from playwright_tests.data.urls import cart_page as cart_page_url
from playwright_tests.data.urls import main_page_url

logger = logging.getLogger(__name__)


class TestCartDeleteFunctionality:
    """Тест-кейсы для проверки удаления четных по порядку товаров из корзины."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, product_page, cart_page):
        self.main_page = main_page
        self.product_page = product_page
        self.cart_page = cart_page
        self.main_page.open(main_page_url)
        yield

    def _add_random_products_from_main_page(self, products_count: int = 5) -> list[str]:
        available_names = {n for n in self.main_page.get_product_names() if n}
        assert len(available_names) >= products_count, (
            f"На главной странице недостаточно уникальных товаров: "
            f"найдено {len(available_names)}, требуется {products_count}."
        )

        added_products = []
        for _ in range(products_count):
            card, product_name = self.main_page.get_random_product_card(
                excluded_product_names=added_products
            )
            self.main_page.open_product_page_from_card(card)
            expect(self.product_page.get_input_quantity()).to_be_visible()
            self.product_page.set_random_quantity()
            self.product_page.click_add_to_cart_button()
            added_products.append(product_name)
            self._return_to_products_page()
        return added_products

    def _return_to_products_page(self) -> None:
        current_url = self.main_page.get_current_url()
        if cart_page_url in current_url:
            self.main_page.go_back()
            self.main_page.go_back()
        else:
            self.main_page.go_back()

        current_url = self.main_page.get_current_url()
        if cart_page_url in current_url or "rt=product/product" in current_url:
            self.main_page.open(main_page_url)

    def test_delete_even_order_items_and_validate_total(self):
        added_products = self._add_random_products_from_main_page(products_count=5)
        assert len(added_products) == 5, "Не удалось добавить 5 товаров в корзину"

        self.main_page.go_to_cart_page()
        cart_data_before = self.cart_page.get_cart_items_data()
        assert len(cart_data_before) == 5, "В корзине должно быть 5 товаров перед удалением"

        total_before = self.cart_page.get_total_price()
        assert total_before is not None and total_before > 0, (
            "Некорректная итоговая стоимость корзины до удаления"
        )

        even_positions = [i for i in range(1, len(cart_data_before) + 1) if i % 2 == 0]
        removed_sum = sum(
            item["price"] * item["quantity"]
            for i, item in enumerate(cart_data_before, start=1)
            if i % 2 == 0
        )

        removed_count = self.cart_page.remove_even_items_by_order()
        assert removed_count == len(even_positions), (
            "Количество удаленных четных товаров не совпадает с ожидаемым"
        )

        cart_data_after = self.cart_page.get_cart_items_data()
        assert len(cart_data_after) == len(cart_data_before) - len(even_positions), (
            "Некорректное количество товаров в корзине после удаления"
        )

        total_after = self.cart_page.get_total_price()
        assert total_after == pytest.approx(total_before - removed_sum, abs=0.01), (
            f"Итоговая стоимость после удаления должна быть {total_before - removed_sum}, "
            f"получено {total_after}"
        )
