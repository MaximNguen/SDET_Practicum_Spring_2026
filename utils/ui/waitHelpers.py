import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)

class WaitHelpers:
    """
    Класс утилитов ожидания элементов
    """

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        """Метод ожидания видимости элемента"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException as e:
            logger.error(
                f"Элемент с локатором {locator} не найден в течение {timeout} секунд. - {e}"
            )

    def wait_for_clickable(self, locator, timeout=10):
        """Метод проверки кликабельности элемента"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException as e:
            logger.error(
                f"Элемент с локатором {locator} не кликабельный в течение {timeout} секунд. - {e}"
            )

    def wait_until_url_change(self, timeout=10, previous_url=None):
        """Метод ожидания изменения URL относительно переданного URL."""
        base_url = previous_url if previous_url is not None else self.driver.current_url
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_changes(base_url))
            return True
        except TimeoutException as e:
            logger.error(f"URL не изменился в течение {timeout} секунд. - {e}")
            return False

    def wait_for_page_load(self, timeout=3):
        """Ожидание полной загрузки страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            return True
        except TimeoutException as e:
            logger.error(f"Страница не загрузилась за {timeout} секунд. - {e}")
            return False

    def wait_until_staleness_of(self, element, timeout=4):
        """Ожидание устаревания элемента."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.staleness_of(element))
            return True
        except TimeoutException as e:
            logger.error(f"Элемент не устарел в течение {timeout} секунд. - {e}")
            return False
        
    def wait_until_logo_available(self, locator, timeout=10):
        """Ожидание появления логотипа на странице."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException as e:
            logger.error(f"Логотип не появился в течение {timeout} секунд. - {e}")
            return False