from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Элемент с локатором {locator} не найден в течение {timeout} секунд.")
            return None
        
    def wait_for_clickable(self, locator, timeout=10):
        """Метод проверки кликабельности элемента"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            print(f"Элемент с локатором {locator} не кликабельный в течение {timeout} секунд.")
            return None
        
    def wait_until_url_change(self, timeout=10):
        """Метод ожидания изменения URL"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_changes(self.driver.current_url)
            )
            return True
        except TimeoutException:
            print(f"URL не изменился в течение {timeout} секунд.")
            return False
        
    def wait_for_page_load(self, timeout=10):
        """Ожидание полной загрузки страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            print(f"Страница не загрузилась за {timeout} секунд.")
            return False