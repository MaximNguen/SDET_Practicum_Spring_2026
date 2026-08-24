import logging
import random

from playwright.sync_api import Locator, Page

from playwright_tests.data.locators import ProductPageLocators as PPL
from playwright_tests.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """Класс для взаимодействия со страницей товара."""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_input_quantity(self) -> Locator:
        return self.page.locator(PPL.input_quantity)

    def set_random_quantity(self, min_value: int = 1, max_value: int = 10) -> None:
        random_quantity = random.randint(min_value, max_value)
        self.get_input_quantity().fill(str(random_quantity))

    def get_add_to_cart_button(self) -> Locator:
        return self.page.locator(PPL.add_to_cart_button)

    def has_radio_options(self) -> bool:
        return self.page.locator(PPL.option_radio_buttons).count() > 0

    def select_first_available_radio_option(self) -> bool:
        radios = self.page.locator(PPL.option_radio_buttons)
        for i in range(radios.count()):
            radio = radios.nth(i)
            if radio.is_enabled():
                radio.check()
                return True
        return False

    def click_add_to_cart_button(self) -> None:
        if self.has_radio_options():
            self.select_first_available_radio_option()
        self.get_add_to_cart_button().click()
        self.page.wait_for_load_state()
