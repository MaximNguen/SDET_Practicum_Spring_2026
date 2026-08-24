import logging
import random
from typing import List

from playwright.sync_api import Locator, Page

from playwright_tests.data.locators import MainPageLocators as MPL
from playwright_tests.data.mock_data import search_value
from playwright_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class MainPage(BasePage):
    """Класс для взаимодействия с главной страницей."""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_navbar(self) -> Locator:
        return self.page.locator(MPL.navbar_list)

    def get_navbar_items(self) -> List[str]:
        items = [t.strip() for t in self.get_navbar().locator("li").all_inner_texts()]
        return [t for t in items if t and t.upper() != "HOME"]

    def click_category(self, category_name: str) -> None:
        logger.info(f"Кликаем по категории: {category_name}")
        self.get_navbar().get_by_role("link", name=category_name, exact=True).click()
        self.page.wait_for_load_state()

    def get_search_input(self) -> Locator:
        return self.page.locator(MPL.search_input)

    def get_product_cards(self) -> Locator:
        return self.page.locator(MPL.product_cards)

    def get_product_names(self) -> List[str]:
        names = []
        cards = self.get_product_cards()
        for i in range(cards.count()):
            name_loc = cards.nth(i).locator(MPL.product_name)
            if name_loc.count() == 0:
                continue
            names.append(name_loc.inner_text().strip())
        return names

    def get_product_name_from_card(self, card: Locator) -> str:
        return card.locator(MPL.product_name).inner_text().strip()

    def get_random_product_card(
        self, excluded_product_names: List[str] = None
    ) -> tuple[Locator, str]:
        excluded = excluded_product_names or []
        candidates = []
        cards = self.get_product_cards()
        for i in range(cards.count()):
            card = cards.nth(i)
            name_loc = card.locator(MPL.product_name)
            if name_loc.count() == 0:
                continue
            name = name_loc.inner_text().strip()
            if name and name not in excluded:
                candidates.append((card, name))
        if not candidates:
            raise ValueError("Недостаточно карточек товаров для случайного выбора.")
        return random.choice(candidates)

    def open_product_page_from_card(self, card: Locator) -> None:
        card.locator(MPL.product_name).click()
        self.page.wait_for_load_state()

    def click_add_cart_button(self, card: Locator) -> None:
        card.locator(MPL.product_cart_button).click()
        self.page.wait_for_load_state()

    def enter_search_value(self, search_input: Locator) -> None:
        search_input.fill(search_value)
        search_input.press("Enter")
        self.page.wait_for_load_state()

    def go_to_cart_page(self) -> None:
        self.page.locator(MPL.cart_button).click()
        self.page.wait_for_load_state()
