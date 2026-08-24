import logging
from typing import List

from playwright.sync_api import Locator, Page

from playwright_tests.data.locators import CartPageLocators as CPL
from playwright_tests.pages.base_page import BasePage
from playwright_tests.utils.string_utils import parse_money_value

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Класс для взаимодействия со страницей корзины."""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_table_cart(self) -> Locator:
        return self.page.locator(CPL.table)

    def get_cart_items(self) -> Locator:
        rows = self.get_table_cart().locator(CPL.cart_rows)
        return rows.filter(has=CPL.name_product).filter(has=CPL.quantity_input)

    def get_cart_items_data(self) -> List[dict]:
        rows = self.get_cart_items()
        cart_data = []
        for i in range(rows.count()):
            row = rows.nth(i)
            name = row.locator(CPL.name_product).inner_text().strip()
            quantity_text = row.locator(CPL.quantity_input).input_value()
            price_text = row.locator(CPL.unit_price).first.inner_text()

            try:
                price = parse_money_value(price_text)
            except ValueError:
                logger.error(f"Не удалось распарсить цену товара '{name}': '{price_text}'")
                continue

            try:
                quantity = int(quantity_text)
            except (TypeError, ValueError):
                logger.error(f"Не удалось распарсить количество товара '{name}': '{quantity_text}'")
                continue

            cart_data.append({"name": name, "price": price, "quantity": quantity})
        return cart_data

    def get_total_price(self) -> float:
        total_text = self.page.locator(CPL.total_price).first.inner_text()
        return parse_money_value(total_text)

    def get_lowest_price_item(self) -> dict:
        cart_data = self.get_cart_items_data()
        if not cart_data:
            raise ValueError("В корзине отсутствуют товары для определения минимальной цены.")
        return min(
            cart_data,
            key=lambda x: x["price"] if x["price"] is not None else float("inf"),
        )

    def double_quantity_lowest_price_item(self) -> None:
        lowest = self.get_lowest_price_item()
        self.set_item_quantity(lowest["name"], lowest["quantity"] * 2)

    def set_item_quantity(self, name: str, quantity: int) -> None:
        row = self._find_row_by_name(name)
        qty = row.locator(CPL.quantity_input)
        qty.fill(str(quantity))
        qty.press("Enter")
        self.page.wait_for_load_state()

    def remove_item_by_order(self, position: int) -> None:
        rows = self.get_cart_items()
        count = rows.count()
        if position < 1 or position > count:
            raise ValueError(f"Неверный порядковый номер товара для удаления: {position}")

        row = rows.nth(position - 1)
        remove = row.locator(CPL.remove_item_button)
        if remove.count() == 0:
            raise ValueError(f"Кнопка удаления не найдена для товара с номером {position}")

        remove.first.click()
        self.page.wait_for_load_state()

    def remove_even_items_by_order(self) -> int:
        count = self.get_cart_items().count()
        even_positions = list(range(2, count + 1, 2))
        for position in reversed(even_positions):
            self.remove_item_by_order(position)
        return len(even_positions)

    def _find_row_by_name(self, name: str) -> Locator:
        rows = self.get_cart_items()
        for i in range(rows.count()):
            row = rows.nth(i)
            if row.locator(CPL.name_product).inner_text().strip() == name:
                return row
        raise ValueError(f"Товар '{name}' не найден в корзине.")
