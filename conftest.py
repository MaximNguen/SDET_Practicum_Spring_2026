from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options

from pages.factory_pages.page_factory import PageFactory

@pytest.fixture()
def driver():
    """Фикстура для создания драйвера с параметрами"""
    options = Options()
    
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()
    
@pytest.fixture
def page_factory(driver):
    """Фикстура для фабрики страниц."""
    return PageFactory(driver)

@pytest.fixture
def main_page(page_factory):
    """Фикстура для главной страницы."""
    return page_factory.get_main_page()

@pytest.fixture
def items_page(page_factory):
    """Фикстура для страницы товаров."""
    return page_factory.get_items_page()

@pytest.fixture
def search_page(page_factory):
    """Фикстура для страницы поиска."""
    return page_factory.get_search_page()

@pytest.fixture
def product_page(page_factory):
    """Фикстура для страницы товара."""
    return page_factory.get_product_page()

@pytest.fixture
def cart_page(page_factory):
    """Фикстура для страницы корзины."""
    return page_factory.get_cart_page()

@pytest.fixture
def fresh_main_page(page_factory):
    """Фикстура для новой (сброшенной) главной страницы."""
    page_factory.reset()
    return page_factory.get_main_page()