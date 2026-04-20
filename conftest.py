from selenium import webdriver
import pytest
import allure
from selenium.webdriver.chrome.options import Options

from pages.factory_pages.page_factory import PageFactory


@pytest.fixture()
def driver():
    """Фикстура для создания драйвера с параметрами"""
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()
    
@pytest.fixture(scope="class", autouse=True)
def class_execution_messages(request):
    """Печать сообщений о начале и завершении выполнения тест-класса."""

    print(f"\n========= Начало ==========")

    yield

    print(f"\n========= Конец ==========")


@pytest.fixture
def page_factory(driver):
    """Фикстура для фабрики страниц."""
    return PageFactory(driver)


@pytest.fixture
def main_page(page_factory):
    """Фикстура для главной страницы."""
    return page_factory.main_page


@pytest.fixture
def items_page(page_factory):
    """Фикстура для страницы товаров."""
    return page_factory.items_page


@pytest.fixture
def search_page(page_factory):
    """Фикстура для страницы поиска."""
    return page_factory.search_page


@pytest.fixture
def product_page(page_factory):
    """Фикстура для страницы товара."""
    return page_factory.product_page


@pytest.fixture
def cart_page(page_factory):
    """Фикстура для страницы корзины."""
    return page_factory.cart_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении теста прикрепляет скриншот Selenium к Allure-отчету."""
    outcome = yield
    report = outcome.get_result()

    if not report.failed or getattr(report, "wasxfail", False):
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        screenshot = driver.get_screenshot_as_png()
    except Exception:
        return

    allure.attach(
        screenshot,
        name=f"{item.name}_{report.when}",
        attachment_type=allure.attachment_type.PNG,
    )
