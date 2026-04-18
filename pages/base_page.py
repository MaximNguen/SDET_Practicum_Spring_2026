from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from typing import List
import allure

from utils.waitHelpers import WaitHelpers as WH

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
            self.wait.wait_for_element(locator)
            return self.driver.find_element(*locator)
    
    def click(self, *locator) -> None:
        """Клик по элементу, найденному по локатору."""
        with allure.step(f"Кликаем по элементу с локатором: {locator}"):
            self.wait.wait_for_clickable(locator)
            self.find_element(*locator).click()
        
    def find_elements(self, *locator) -> List[WebElement]:
        """Поиск всех элементов на странице по локатору."""
        with allure.step(f"Находим все элементы с локатором: {locator}"):
            self.wait.wait_for_element(locator)
            return self.driver.find_elements(*locator)
    
    def input_text(self, element: WebElement, text: str):
        """Ввести текст в поле"""
        with allure.step(f"Вводим текст '{text}' в элемент с элементом: {element}"):
            element.clear()
            self.wait.wait_for_clickable(element)
            element.send_keys(text)
            element.send_keys(Keys.ENTER)
        
    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """Получить текст элемента"""
        with allure.step(f"Получаем текст элемента с локатором: {locator}"):
            self.wait.wait_for_element(locator)
            element = self.find_element(locator, timeout)
            return element.text
    
    def scroll(self, element: WebElement):
        """Метод прокрутки до указанного элемента."""
        with allure.step(f"Прокрутить страницу до элемента: {element}"):
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self
    
    def quit(self):
        """Метод выхода из браузера."""
        with allure.step("Закрываем браузер"):
            self.driver.quit()
        return self
    
    def open(self, url: str) -> None:
        """Открыть главную страницу по URL."""
        with allure.step(f"Открываем главную страницу по URL: {url}"):
            self.driver.get(url)
            
    def go_back_page(self) -> None:
        """Вернуться на предыдущую страницу."""
        with allure.step("Возвращаемся на предыдущую страницу"):
            self.driver.back()
            self.wait.wait_until_url_change()
            self.wait.wait_for_page_load()
