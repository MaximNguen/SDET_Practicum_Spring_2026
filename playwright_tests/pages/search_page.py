import logging
from typing import List

from playwright.sync_api import Locator, Page

from playwright_tests.data.locators import SearchPageLocators as SPL
from playwright_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class SearchPage(BasePage):
    """Класс для взаимодействия со страницей поиска."""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_products_cards(self) -> Locator:
        return self.page.locator(SPL.cards)

    def get_products_current_items(self, numbers: List[int]) -> List[Locator]:
        cards = self.get_products_cards()
        return [cards.nth(n - 1) for n in numbers]

    def click_add_cart_button(self, card: Locator) -> None:
        card.locator(SPL.cart_button).click()
        self.page.wait_for_load_state()
