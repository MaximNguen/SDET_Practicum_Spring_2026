import logging
import allure
import pytest
import random

from data.urls import main_page_url
from data.expected_data import expected_categories
from data.mock_data import random_category

logger = logging.getLogger(__name__)

@allure.epic("UI Тесты")
@allure.feature("Тест-кейсы на наличие элементов и их работоспособность")
class TestPositiveResult:
    """Позитивные тест-кейсы для проверки работоспособности элементов сайта."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page, url=main_page_url):
        self.main_page = main_page
        self.items_page = items_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()

    @allure.title("Проверка наличия навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка наличия навигационной панели на главной странице и ее видимости.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент навигационной панели на странице.\n
        2. Проверить, что элемент отображается на странице.\n
        Ожидаемый результат - Навигационная панель присутствует на странице и видима для пользователя."""
        )
    def test_get_navbar(self):
        logger.info("Проверяем наличие навигационной панели")
        nav = self.main_page.get_navbar()
        assert nav.is_displayed(), "Не отображается панель навигационная"

    @allure.title("Проверка наличия поля ввода поиска на главной странице")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка наличия поля ввода поиска на главной странице.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент поля ввода поиска на странице.\n
        2. Проверить, что элемент отображается на странице.\n
        Ожидаемый результат - Поле ввода поиска присутствует на странице и видимо для пользователя."""
        )
    def test_get_search_input(self):
        logger.info("Проверяем наличие поля ввода поиска на главной странице")
        search_input = self.main_page.get_search_input()
        assert search_input.is_displayed(), "Не отображается поле ввода поиска на главной странице"

    @allure.title("Проверка наличия фильтра товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        """Проверка наличия фильтра товаров.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент навигационной панели на странице.\n
        2. Проверить, что элемент отображается на странице.\n
        3. Кликнуть по одной из категорий в навигационной панели.\n
        4. Найти элемент фильтра товаров на странице категории.\n
        5. Проверить, что элемент отображается на странице.\n
        Ожидаемый результат - Фильтр товаров присутствует на странице и видим для пользователя."""
        )
    def test_get_filter(self):
        """Проверка наличия фильтра товаров."""
        logger.info("Проверяем наличие фильтра товаров")
        category = random.choice(random_category)
        with allure.step("Переходим на страницу 1 из категорий"):
            self.main_page.click_category(category)

        with allure.step("Проверяем наличие фильтра"):
            filter = self.items_page.get_filter_select()
            assert filter.is_displayed(), "Фильтр не отображается на сайте"
        
    @allure.title("Проверка наличия категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка наличия категорий в навигационной панели.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент навигационной панели на странице.\n
        2. Проверить каждый элемент на панели.\n
        3. Проверить, что все ожидаемые категории присутствуют в навигационной панели.\n
        Ожидаемый результат - Все ожидаемые категории присутствуют в навигационной панели и видимы для пользователя."""
        )
    def test_navbar_categories(self):
        """Проверка наличия категорий в навигационной панели."""
        logger.info("Проверяем наличие категорий в навигационной панели")
        categories = self.main_page.get_navbar_items()
        for category in expected_categories:
            with allure.step(f"Проверяем наличие категории: {category}"):
                assert category.upper() in categories, f"Категория '{category}' не найдена в навигационной панели."
                
    @allure.title("Проверка кликабельности категорий в навигационной панели")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка кликабельности категории в навигационной панели.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент навигационной панели на странице.\n
        2. Проверить каждый элемент на панели.\n
        3. Кликнуть по одной из категорий.\n
        4. Проверить, что после клика происходит переход на страницу категории.\n
        Ожидаемый результат - 1 из категорий в навигационной панели кликабельна, и при клике происходит переход на соответствующую страницу категории."""
        )
    def test_click_random_category(self):
        """Проверка кликабельности категорий в навигационной панели."""
        logger.info("Проверяем кликабельность категорий в навигационной панели")
        category = random.choice(random_category)
        with allure.step(f"Проверяем кликабельность категории: {category}"):
            self.main_page.click_category(category)
            current_url = self.main_page.driver.current_url
            assert current_url != main_page_url, \
                f"Клик по категории '{category}' не привел к переходу"
                    
    @allure.title("Проверка кликабельности всех категорий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка кликабельности всех категорий в навигационной панели.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Найти элемент навигационной панели на странице.\n
        2. Проверить каждый элемент на панели.\n
        3. Кликнуть по каждой категории.\n
        4. Проверить, что после клика происходит переход на страницу категории.\n
        Ожидаемый результат - Все кнопки категорий в навигационной панели кликабельны, и при клике происходит переход на соответствующую страницу категории."""
        )
    def test_click_all_categories(self):
        """Проверка кликабельности каждой категории в навигационной панели."""
        logger.info("Проверяем кликабельность всех категорий в навигационной панели")
        categories = self.main_page.get_navbar_items()
        
        for category in categories:
            with allure.step(f"Кликаем и проверяем категорию: {category}"):
                self.main_page.click_category(category)
                
                current_url = self.main_page.driver.current_url
                assert current_url != main_page_url, \
                    f"Клик по категории '{category}' не привел к переходу"
                
                self.main_page.open(main_page_url)
                
    @allure.title("Проверка наличия товаров на странице категории")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        """Проверка наличия товаров на странице категории.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элементы карточек товаров на странице категории.\n
        3. Проверить, что карточки товаров присутствуют на странице категории.\n
        Ожидаемый результат - На странице категории присутствуют карточки товаров, видимые для пользователя."""
        )
    def test_category_products(self):
        """Проверка наличия товаров на странице категории."""
        logger.info("Проверяем наличие товаров на странице категории")
        category = random.choice(random_category)
        with allure.step(f"Проверяем наличие товаров в категории: {category}"):
            self.main_page.click_category(category)
            products_data = self.items_page.get_products_cards()
            assert products_data, f"На странице категории '{category}' не найдено товаров."
            
    @allure.title("Проверка кликабельности сортировки товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        """Проверка кликабельности сортировки товаров.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Кликнуть по одной из категорий в навигационной панели.\n
        2. Найти элемент фильтра товаров на странице категории.\n
        3. Проверить, что элемент отображается на странице категории.\n
        4. Кликнуть по элементу фильтра товаров.\n
        5. Проверить, что после клика происходит сортировка товаров на странице категории.\n
        Ожидаемый результат - Фильтр товаров кликабельный, и при клике происходит сортировка товаров на странице категории."""
        )
    def test_sorting_products(self):
        """Проверка кликабельности сортировки товаров."""
        logger.info("Проверяем кликабельность сортировки товаров")
        category = random.choice(random_category)
        with allure.step(f"Проверяем сортировку товаров в категории: {category}"):
            self.main_page.click_category(category)
            self.items_page.select_filter_option("Price Low > High")
            products_data = self.items_page.get_products_prices()
            assert products_data, f"На странице категории '{category}' не найдено товаров."
