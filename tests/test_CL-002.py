import allure
import pytest

from data.urls import main_page_url
from data.mock_data import search_value


@allure.epic("Выполнение Чек-листа 002 - Проверка добавления товара в корзину, поиск товаров и изменение корзины")
@allure.feature("Тест-кейсы для проверки добавления товара в корзину, поиск товаров и изменение корзины")
class TestSearchAndCartFunctionality:
    """Тест-кейсы для проверки добавления товара в корзину, поиск товаров и изменение корзины."""

    @pytest.fixture(autouse=True)
    def setup(
        self,
        main_page,
        items_page,
        product_page,
        cart_page,
        search_page,
        url=main_page_url,
    ):
        self.main_page = main_page
        self.items_page = items_page
        self.product_page = product_page
        self.cart_page = cart_page
        self.search_page = search_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()

    def _add_product_to_cart_from_search(self, position: int) -> None:
        """Найти товар в выдаче поиска по позиции и добавить его в корзину."""
        search_input = self.main_page.get_search_input()
        self.main_page.enter_search_value(search_input)
        cards = self.search_page.get_products_current_items([position])

        assert (
            len(cards) == 1
        ), f"Не найдена карточка товара с позицией {position} для добавления в корзину."

        self.search_page.click_add_cart_button(cards[0])
        input_quantity = self.product_page.get_input_quantity()

        assert (
            input_quantity.is_displayed()
        ), "Не отображается поле ввода количества товара на странице товара"

        self.product_page.set_random_quantity()
        self.product_page.click_add_to_cart_button()

    @allure.story("Проверка наличия поля для ввода поиска на главной странице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_search_input(self):
        """Проверка наличия поля для ввода поиска на главной странице."""
        search_input = self.main_page.get_search_input()
        assert (
            search_input.is_displayed()
        ), "Не отображается поле ввода поиска на главной странице"

    @allure.story("Проверка результатов поиска после ввода текста")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_search_results(self):
        """Проверка результатов поиска после ввода текста."""
        search_input = self.main_page.get_search_input()
        with allure.step(
            f"Вводим текст '{search_value}' в поле поиска и проверяем результаты"
        ):
            self.main_page.enter_search_value(search_input)
            results = self.search_page.get_products_cards()
            assert results, f"По запросу '{search_value}' не найдено товаров."

    @allure.story("Проверка наличия товаров в корзине после добавления")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_add_to_cart_button(self):
        """Проверка наличия товаров в корзине после добавления."""
        for position in [2, 3]:
            with allure.step(
                f"Добавляем в корзину товар из результата поиска с позицией {position}"
            ):
                self._add_product_to_cart_from_search(position)
                self.main_page.open(main_page_url)

        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, "В корзине не найдено товаров после добавления."

    @allure.story("Проверка изменения товаров в корзине после добавления")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_quantity_for_lowest(self):
        """Проверка изменения товаров в корзине после добавления."""
        for position in [2, 3]:
            with allure.step(
                f"Добавляем в корзину товар из результата поиска с позицией {position}"
            ):
                self._add_product_to_cart_from_search(position)
                self.main_page.open(main_page_url)

        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, "В корзине не найдено товаров после добавления."

        total_price = self.cart_page.get_total_price()
        assert (
            total_price > 0
        ), "Общая стоимость товаров в корзине не отображается или равна нулю."

        lowest_data = self.cart_page.get_lowest_price_item()
        self.cart_page.double_quantity_lowest_price_item()
        new_total_price = self.cart_page.get_total_price()

        assert (
            new_total_price > total_price
        ), "Общая стоимость товаров в корзине не изменилась после изменения количества товара с самой низкой ценой."

        new_data = lowest_data["quantity"] * lowest_data["price"]
        assert (
            new_total_price == total_price + new_data
        ), "Общая стоимость товаров в корзине не изменилась на сумму удвоенного количества товара с самой низкой ценой."
