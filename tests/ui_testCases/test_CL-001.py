import allure
import pytest
import random
import logging

from data.ui_data.urls import main_page_url
from data.ui_data.expected_data import expected_categories

logger = logging.getLogger(__name__)

@allure.epic("Выполнение Чек-листа 001 - Проверка фильтра товаров")
@allure.feature("Тест-кейсы для проверки производительности фильтра товаров")
class TestFilterPerformance:
    """Тест-кейсы для проверки производительности фильтра товаров."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page, url=main_page_url):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()

    @allure.title("Проверка наличия товаров всех категориях и количество товаров не меньше 4")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка наличия товаров в каждой категории и количество товаров не меньше 4.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элементы карточек товаров на странице категории.\n
        3. Проверить, что карточки товаров присутствуют на странице категории.\n
        Ожидаемый результат - На странице категории присутствуют карточки товаров, видимые для пользователя."""
        )
    def test_check_products_in_category(self):
        """Проверка наличия товаров в каждой категории и количество товаров не меньше 4."""
        logger.info("Проверяем наличие товаров в каждой категории и количество товаров не меньше 4")
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем наличие товаров в категории: {category}"):
                logger.info(f"Проверяем наличие товаров в категории: {category}")
                self.main_page.click_category(category)
                current_url = self.main_page.get_current_url()
                assert (
                    current_url != main_page_url
                ), f"Клик по категории '{category}' не привел к переходу"
                products_data = self.items_page.get_products_names()
                logger.info(f"Получаем данные о товарах в категории: {category}")
                assert (
                    products_data
                ), f"На странице категории '{category}' не найдено товаров."
                assert (
                    len(products_data) >= 4
                ), f"На странице категории '{category}' найдено меньше 4 товаров."

    @allure.title("Проверка кликабельности сортировки товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка кликабельности сортировки товаров.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Проверить, что элемент отображается на странице категории.\n
        Ожидаемый результат - Фильтр товаров отображается на странице категории."""
        )
    def test_check_filter_performance(self):
        """Проверка кликабельности сортировки товаров."""
        category = random.choice(expected_categories)
        with allure.step("Переходим на страницу 1 из категорий"):
            logger.info("Переходим на страницу 1 из категорий")
            self.main_page.click_category(category)
            current_url = self.main_page.get_current_url()
            assert (
                current_url != main_page_url
            ), f"Клик по категории '{category}' не привел к переходу"
        with allure.step(
            f"Проверяем наличие сортировку товаров в категории: {category}"
        ):
            logger.info(f"Проверяем наличие сортировку товаров в категории: {category}")

            select = self.items_page.get_filter_select()
            assert select.is_displayed(), "Фильтр не отображается на сайте"

    @allure.title("Проверка сортировки товаров по цене от дешевых к дорогим")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка сортировки товаров по цене от дешевых к дорогим.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Выбрать сортировку товаров по цене от дешевых к дорогим.\n
        4. Получить данные о ценах товаров на странице категории.\n
        5. Проверить, что товары отсортированы по цене от дешевых к дорогим.\n
        Ожидаемый результат - Товары в категории отсортированы по цене от дешевых к дорогим."""
        )
    def test_check_filter_sorting_price_asc(self):
        """Проверка сортировки товаров по цене от дешевых к дорогим."""
        logger.info("Проверяем сортировку товаров по цене от дешевых к дорогим")
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                logger.info(f"Проверяем сортировку товаров в категории: {category}")
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Price Low > High")
                products_data = self.items_page.get_products_prices()
                current_url = self.main_page.get_current_url()

                assert (
                    current_url != main_page_url
                ), f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(
                    products_data
                ), f"Товары в категории '{category}' не отсортированы по цене от дешевых к дорогим."

    @allure.title("Проверка сортировки товаров по цене от дорогих к дешевым")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка сортировки товаров по цене от дорогих к дешевым.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Выбрать сортировку товаров по цене от дорогих к дешевым.\n
        4. Получить данные о ценах товаров на странице категории.\n
        5. Проверить, что товары отсортированы по цене от дорогих к дешевым.\n
        Ожидаемый результат - Товары в категории отсортированы по цене от дорогих к дешевым."""
        )

    def test_check_filter_sorting_price_desc(self):
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                logger.info(f"Проверяем сортировку товаров в категории: {category}")
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Price High > Low")
                products_data = self.items_page.get_products_prices()
                current_url = self.main_page.get_current_url()

                assert (
                    current_url != main_page_url
                ), f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(
                    products_data, reverse=True
                ), f"Товары в категории '{category}' не отсортированы по цене от дорогих к дешевым."

    @allure.title("Проверка сортировки товаров по названию от A до Z")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка сортировки товаров по названию от A до Z.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Выбрать сортировку товаров по названию от A до Z.\n
        4. Получить данные о названиях товаров на странице категории.\n
        5. Проверить, что товары отсортированы по названию от A до Z.\n
        Ожидаемый результат - Товары в категории отсортированы по названию от A до Z."""
        )
    def test_check_filter_sorting_name_asc(self):
        logger.info("Проверяем сортировку товаров по названию от A до Z")
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                logger.info(f"Проверяем сортировку товаров в категории: {category}")
                self.main_page.click_category(category)
                current_url = self.main_page.get_current_url()
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Name A - Z")
                products_data = self.items_page.get_products_names()

                assert (
                    current_url != main_page_url
                ), f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(
                    products_data
                ), f"Товары в категории '{category}' не отсортированы по названию от A до Z."

    @allure.title("Проверка сортировки товаров по названию от Z до A")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка сортировки товаров по названию от Z до A.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Выбрать сортировку товаров по названию от Z до A.\n
        4. Получить данные о названиях товаров на странице категории.\n
        5. Проверить, что товары отсортированы по названию от Z до A.\n
        Ожидаемый результат - Товары в категории отсортированы по названию от Z до A."""
        )
    def test_check_filter_sorting_name_desc(self):
        logger.info("Проверяем сортировку товаров по названию от Z до A")
        categories = self.main_page.get_navbar_items()
        for category in categories:
            with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
                logger.info(f"Проверяем сортировку товаров в категории: {category}")
                self.main_page.click_category(category)
                cards = self.items_page.get_products_cards()
                self.items_page.select_filter_option("Name Z - A")
                products_data = self.items_page.get_products_names()
                current_url = self.main_page.get_current_url()

                assert (
                    current_url != main_page_url
                ), f"Клик по категории '{category}' не привел к переходу"
                assert cards, f"На странице категории '{category}' не найдено товаров."
                assert products_data == sorted(
                    products_data, reverse=True
                ), f"Товары в категории '{category}' не отсортированы по названию от Z до A."
