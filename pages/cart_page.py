from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from data.locators_cart import CartPageLocators as CPL
from pages.base_page import BasePage
from utils.stringUtils import StringUtils as SU


class CartPage(BasePage):
    """
    Класс для взаимодействия со страницей корзины.
    Содержит методы для работы с элементами страницы.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def get_table_cart(self) -> WebElement:
        """Получить элемент таблицы корзины."""
        with allure.step("Получаем элемент таблицы корзины"):
            table = self.find_element(*CPL.table)
            self.scroll(table)
            return table

    def get_cart_items(self) -> List[WebElement]:
        """Получить элементы строк товаров в корзине."""
        with allure.step("Получаем элементы строк товаров в корзине"):
            table = self.get_table_cart()
            rows = table.find_elements(*CPL.cart_rows)
            items = []
            for row in rows:
                has_name = bool(row.find_elements(*CPL.name_product))
                has_quantity = bool(row.find_elements(*CPL.quantity_input))
                if has_name and has_quantity:
                    items.append(row)
            return items

    def get_cart_items_data(self) -> List[dict]:
        """Получить данные о товарах в корзине."""
        with allure.step("Получаем данные о товарах в корзине"):
            items = self.get_cart_items()
            cart_data = []
            for item in items:
                name = self.get_text_from_child(item, *CPL.name_product)
                quantity_value = self.get_attribute_from_child(
                    item,
                    *CPL.quantity_input,
                    attribute="value",
                )
                price_text = self.get_text_from_child(item, *CPL.unit_price)

                try:
                    price = SU._parse_money_value(price_text)
                except ValueError:
                    continue

                try:
                    quantity = int(quantity_value)
                except (TypeError, ValueError):
                    continue

                cart_data.append({"name": name, "price": price, "quantity": quantity})
            return cart_data

    def get_total_price(self) -> float:
        """Получить общую стоимость товаров в корзине."""
        with allure.step("Получаем общую стоимость товаров в корзине"):
            total_element = self.find_element(*CPL.total_price)
            self.scroll(total_element)
            try:
                total_price = SU._parse_money_value(total_element.text)
                return total_price
            except ValueError:
                return None

    def get_lowest_price_item(self) -> dict:
        """Получить товар с самой низкой ценой в корзине."""
        with allure.step("Получаем товар с самой низкой ценой в корзине"):
            cart_data = self.get_cart_items_data()
            if not cart_data:
                raise ValueError(
                    "В корзине отсутствуют товары для определения минимальной цены."
                )
            lowest_price_item = min(
                cart_data,
                key=lambda x: x["price"] if x["price"] is not None else float("inf"),
            )
            return lowest_price_item

    def get_item_input_quantity_lowest_price(self) -> WebElement:
        """Получить элемент поля количества для товара с самой низкой ценой в корзине."""
        with allure.step(
            "Получаем элемент поля количества для товара с самой низкой ценой в корзине"
        ):
            lowest_price_item = self.get_lowest_price_item()
            items = self.get_cart_items()
            for item in items:
                name = self.get_text_from_child(item, *CPL.name_product)
                if name == lowest_price_item["name"]:
                    quantity_input = item.find_element(*CPL.quantity_input)
                    self.scroll(quantity_input)
                    return quantity_input
            return None

    def double_quantity_lowest_price_item(self) -> None:
        """Удвоить количество товара с самой низкой ценой в корзине."""
        with allure.step("Удваиваем количество товара с самой низкой ценой в корзине"):
            quantity_input = self.get_item_input_quantity_lowest_price()
            if quantity_input:
                current_value = quantity_input.get_attribute("value")
                try:
                    current_quantity = int(current_value)
                    new_quantity = current_quantity * 2
                    self.input_text(quantity_input, text=str(new_quantity))
                    self.input_enter(quantity_input)
                except ValueError:
                    pass

    def remove_item_by_order(self, position: int) -> None:
        """Удалить товар из корзины по номеру."""
        with allure.step(f"Удаляем товар из корзины по порядковому номеру {position}"):
            items = self.get_cart_items()
            if position < 1 or position > len(items):
                raise ValueError(
                    f"Неверный порядковый номер товара для удаления: {position}"
                )

            row = items[position - 1]
            remove_buttons = row.find_elements(*CPL.remove_item_button)
            if not remove_buttons:
                raise ValueError(
                    f"Кнопка удаления не найдена для товара с номером {position}"
                )

            self.scroll(remove_buttons[0])
            remove_buttons[0].click()

            try:
                WebDriverWait(self.driver, 4).until(EC.staleness_of(row))
            except TimeoutException:
                self.wait.wait_for_page_load(timeout=2)

    def remove_even_items_by_order(self) -> int:
        """Удалить из корзины все товары с четными порядковыми номерами."""
        with allure.step(
            "Удаляем из корзины все товары с четными порядковыми номерами"
        ):
            items_count = len(self.get_cart_items())
            even_positions = list(range(2, items_count + 1, 2))

            removed_count = 0
            for position in reversed(even_positions):
                self.remove_item_by_order(position)
                removed_count += 1

            return removed_count
