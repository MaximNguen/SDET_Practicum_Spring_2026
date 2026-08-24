import logging
from typing import List

from playwright.sync_api import Locator, Page

from playwright_tests.data.locators import ItemPageLocators as IPL
from playwright_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ItemPage(BasePage):
    """Класс для взаимодействия со страницей товаров."""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_filter_select(self) -> Locator:
        return self.page.locator(IPL.filter_select)

    def select_filter_option(self, option_text: str) -> None:
        self.get_filter_select().select_option(label=option_text)
        self.page.wait_for_load_state()

    def get_product_cards(self) -> Locator:
        return self.page.locator(IPL.cards)

    def get_products_prices(self) -> List[float]:
        prices = []
        cards = self.get_product_cards()
        for i in range(cards.count()):
            card = cards.nth(i)
            price_loc = card.locator(IPL.price_product)
            if price_loc.count() == 0:
                price_loc = card.locator(IPL.price_product_new)
            if price_loc.count() == 0:
                logger.error("Не найден элемент цены у товара")
                continue
            price_text = price_loc.inner_text().replace("$", "")
            try:
                prices.append(float(price_text))
            except ValueError:
                logger.error(f"Не удалось распарсить цену товара: '{price_text}'")
                continue
        return prices

    def get_products_names(self) -> List[str]:
        names = []
        cards = self.get_product_cards()
        for i in range(cards.count()):
            name = cards.nth(i).locator(IPL.name_product).inner_text().strip()
            if name:
                names.append(name)
        return names
