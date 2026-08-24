import sys
from pathlib import Path

import pytest
from playwright.sync_api import Page

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from playwright_tests.pages.cart_page import CartPage
from playwright_tests.pages.items_page import ItemPage
from playwright_tests.pages.main_page import MainPage
from playwright_tests.pages.product_page import ProductPage
from playwright_tests.pages.search_page import SearchPage


@pytest.fixture
def main_page(page: Page) -> MainPage:
    return MainPage(page)


@pytest.fixture
def items_page(page: Page) -> ItemPage:
    return ItemPage(page)


@pytest.fixture
def search_page(page: Page) -> SearchPage:
    return SearchPage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)
