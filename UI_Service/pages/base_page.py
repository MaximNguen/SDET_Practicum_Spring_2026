from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import allure
import logging

from utils.ui.waitHelpers import WaitHelpers as WH
from utils.ui.locatorUtils import LocatorUtils as LU

logger = logging.getLogger(__name__)

class BasePage:
    """
    Базовая страница для всех страниц приложения.
    Содержит общие методы для взаимодействия
    с элементами страницы.
    """

    def __init__(self, driver):
        """Инициализация драйвера"""
        self.driver = driver
        self.wait = WH(self.driver)

    def find_element(self, *locator) -> WebElement:
        """Поиск элемента на странице по локатору."""
        with allure.step(f"Находим элемент с локатором: {locator}"):
            logger.info(f"Находим элемент с локатором: {locator}")
            locator = LU.normalize_locator(locator)
            elem = self.wait.wait_for_element(locator)
            self.scroll(elem)
            return self.driver.find_element(*locator)

    def click(self, *locator) -> None:
        """Клик по элементу, найденному по локатору."""
        with allure.step(f"Кликаем по элементу с локатором: {locator}"):
            logger.info(f"Кликаем по элементу с локатором: {locator}")
            self.wait.wait_for_clickable(locator)
            self.find_element(*locator).click()

    def find_elements(self, *locator) -> List[WebElement]:
        """Поиск всех элементов на странице по локатору."""
        with allure.step(f"Находим все элементы с локатором: {locator}"):
            logger.info(f"Находим все элементы с локатором: {locator}")
            locator = LU.normalize_locator(locator)
            self.wait.wait_for_element(locator)
            return self.driver.find_elements(*locator)

    def input_text(self, element: WebElement, text: str):
        """Ввести текст в поле."""
        with allure.step(f"Вводим текст '{text}' в элемент с элементом: {element}"):
            logger.info(f"Вводим текст '{text}' в элемент с элементом: {element}")
            element.clear()
            self.wait.wait_for_clickable(element)
            element.send_keys(text)

    def input_enter(self, element: WebElement):
        """Нажать Enter в поле."""
        with allure.step(f"Нажимаем Enter в элементе: {element}"):
            logger.info(f"Нажимаем Enter в элементе: {element}")
            self.wait.wait_for_clickable(element)
            element.send_keys(Keys.ENTER)

    def get_text(self, *locator) -> str:
        """Получить текст элемента"""
        with allure.step(f"Получаем текст элемента с локатором: {locator}"):
            logger.info(f"Получаем текст элемента с локатором: {locator}")
            locator = LU.normalize_locator(locator)
            element = self.find_element(*locator)
            element = element.text.strip()
            return element

    def get_text_from_element(self, element: WebElement) -> str:
        """Получить текст из WebElement"""
        with allure.step(f"Получаем текст из элемента: {element}"):
            logger.info(f"Получаем текст из элемента: {element}")
            return element.text.strip()

    def get_attribute_data(self, *locator, attribute: str) -> str:
        """Получить атрибут элемента"""
        with allure.step(
            f"Получаем атрибут '{attribute}' элемента с локатором: {locator}"
        ):
            logger.info(f"Получаем атрибут '{attribute}' элемента с локатором: {locator}")
            locator = LU.normalize_locator(locator)
            element = self.find_element(*locator)
            return element.get_attribute(attribute)

    def find_child_element(self, parent: WebElement, *locator) -> WebElement:
        """Найти дочерний элемент внутри переданного WebElement."""
        with allure.step(f"Находим дочерний элемент с локатором: {locator}"):
            logger.info(f"Находим дочерний элемент с локатором: {locator}")
            locator = LU.normalize_locator(locator)
            element = parent.find_element(*locator)
            self.scroll(element)
            return element

    def get_text_from_child(self, parent: WebElement, *locator) -> str:
        """Получить текст дочернего элемента внутри WebElement."""
        with allure.step(f"Получаем текст дочернего элемента с локатором: {locator}"):
            logger.info(f"Получаем текст дочернего элемента с локатором: {locator}")
            element = self.find_child_element(parent, *locator)
            return self.get_text_from_element(element)

    def get_attribute_from_child(
        self, parent: WebElement, *locator, attribute: str
    ) -> str:
        """Получить атрибут дочернего элемента внутри WebElement."""
        with allure.step(
            f"Получаем атрибут '{attribute}' дочернего элемента с локатором: {locator}"
        ):
            logger.info(f"Получаем атрибут '{attribute}' дочернего элемента с локатором: {locator}")
            element = self.find_child_element(parent, *locator)
            return element.get_attribute(attribute)

    def scroll(self, element: WebElement):
        """Метод прокрутки до указанного элемента."""
        with allure.step(f"Прокрутить страницу до элемента: {element}"):
            logger.info(f"Прокрутить страницу до элемента: {element}")
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self

    def quit(self):
        """Метод выхода из браузера."""
        with allure.step("Закрываем браузер"):
            logger.info("Закрываем браузер")
            self.driver.quit()
        return self

    def open(self, url: str) -> None:
        """Открыть главную страницу по URL."""
        with allure.step(f"Открываем главную страницу по URL: {url}"):
            logger.info(f"Открываем главную страницу по URL: {url}")
            self.driver.get(url)

    def go_back_page(self) -> None:
        """Вернуться на предыдущую страницу."""
        with allure.step("Возвращаемся на предыдущую страницу"):
            logger.info("Возвращаемся на предыдущую страницу")
            previous_url = self.get_current_url()
            self.driver.back()
            url_changed = self.wait.wait_until_url_change(previous_url=previous_url)

            if not url_changed and self.get_current_url() == previous_url:
                self.driver.execute_script("window.history.go(-1)")
                self.wait.wait_until_url_change(previous_url=previous_url)

            self.wait.wait_for_page_load()

    def get_current_url(self) -> str:
        """Получить текущий URL страницы."""
        with allure.step("Получаем текущий URL страницы"):
            logger.info("Получаем текущий URL страницы")
            return self.driver.current_url

    def check_radio(self) -> bool:
        """Проверить наличие radio-options на странице."""
        with allure.step("Проверяем наличие radio-options на странице"):
            logger.info("Проверяем наличие radio-options на странице")
            return bool(
                self.driver.execute_script(
                    "return document.querySelectorAll(\"input[type='radio'][name^='option']\").length;"
                )
            )