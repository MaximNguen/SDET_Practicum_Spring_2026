import allure
import pytest
import logging

from data.urls import main_page_url

logger = logging.getLogger(__name__)

@allure.epic("Выполнение Чек-листа 003 - Проверка удаления товаров из корзины")
@allure.feature("Тест-кейсы для удаления четных по порядку товаров из корзины")
class TestCartDeleteFunctionality:
    """Тест-кейсы для проверки удаления четных по порядку товаров из корзины."""

    @pytest.fixture(autouse=True)
    def setup(self, main_page, product_page, cart_page, url=main_page_url):
        self.main_page = main_page
        self.product_page = product_page
        self.cart_page = cart_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()

    def _add_random_products_from_main_page(self, products_count: int = 5) -> list[str]:
        """Добавить в корзину указанное количество случайных товаров с главной страницы."""
        logger.info("Добавляем случайные товары с главной страницы")
        cards = self.main_page.get_products_cards()
        available_names = {
            self.main_page.get_product_name_from_card(card) for card in cards
        }
        available_names = {name for name in available_names if name}

        assert len(available_names) >= products_count, (
            f"На главной странице недостаточно уникальных товаров для добавления: "
            f"найдено {len(available_names)}, требуется {products_count}."
        )

        added_products = []
        for index in range(products_count):
            logger.info(f"Добавляем товар с позицией {index + 1}")
            if index > 0:
                self.main_page.open(main_page_url)
            card, product_name = self.main_page.get_random_product_card(
                excluded_product_names=added_products
            )
            self.main_page.open_product_page_from_card(card)

            input_quantity = self.product_page.get_input_quantity()
            assert (
                input_quantity.is_displayed()
            ), "Не отображается поле ввода количества товара на странице товара"

            self.product_page.set_random_quantity()
            self.product_page.click_add_to_cart_button()

            added_products.append(product_name)

        return added_products

    @allure.title("Добавление 5 случайных товаров и удаление четных по порядку")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Добавление 5 случайных товаров с главной страницы и удаление товаров с четными порядковыми номерами в корзине.\n
        Предусловие - Открыть главную страницу сайта.\n
        Шаги:\n
        1. Получить данные о карточках товаров на главной странице.\n
        2. Добавить в корзину 5 случайных товаров с главной страницы.\n
        3. Выбрав 1 из карточек товаров, перейти на страницу товара\n
        4. На странице товара установить случайное количество и добавить товар в корзину\n
        5. Добавить название товарал в список добавленных товаров\n
        6. Повторить шаги 3-5, пока в корзине не будет 5 товаров\n
        7. Перейти в корзину и считать данные о товарах до удаления\n
        8. Удалить товары с четными порядковыми номерами\n
        9. Проверить, что количество товаров в корзине уменьшилось на количество удаленных товаров\n
        10. Проверить, что итоговая стоимость корзины уменьшилась на сумму удаленных товаров\n
        Ожидаемый результат - Товары с четными порядковыми номерами удалены из корзины, количество товаров в корзине уменьшилось на количество удаленных товаров, 
        итоговая стоимость корзины уменьшилась на сумму удаленных товаров."""
        )
    def test_delete_even_order_items_and_validate_total(self):
        """Добавить 5 случайных товаров и удалить все четные по порядку с проверкой суммы."""
        logger.info("Добавляем 5 случайных товаров и удаляем все четные по порядку с проверкой суммы")
        with allure.step("Добавляем в корзину 5 случайных товаров с главной страницы"):
            added_products = self._add_random_products_from_main_page(products_count=5)
            assert len(added_products) == 5, "Не удалось добавить 5 товаров в корзину"

        with allure.step("Переходим в корзину и считываем данные до удаления"):
            logger.info("Переходим в корзину и считываем данные до удаления")
            self.main_page.go_to_cart_page()
            cart_data_before = self.cart_page.get_cart_items_data()
            assert (
                len(cart_data_before) == 5
            ), "В корзине должно быть 5 товаров перед удалением"

            total_before = self.cart_page.get_total_price()
            assert (
                total_before is not None and total_before > 0
            ), "Некорректная итоговая стоимость корзины до удаления"

        with allure.step("Удаляем товары с четными порядковыми номерами"):
            logger.info("Удаляем товары с четными порядковыми номерами")
            even_positions = [
                index for index in range(1, len(cart_data_before) + 1) if index % 2 == 0
            ]
            removed_sum = sum(
                item["price"] * item["quantity"]
                for index, item in enumerate(cart_data_before, start=1)
                if index % 2 == 0
            )

            removed_count = self.cart_page.remove_even_items_by_order()
            assert removed_count == len(
                even_positions
            ), "Количество удаленных четных товаров не совпадает с ожидаемым"

        with allure.step(
            "Проверяем итоговую стоимость и количество товаров после удаления"
        ):
            logger.info("Проверяем итоговую стоимость и количество товаров после удаления")
            cart_data_after = self.cart_page.get_cart_items_data()
            expected_items_after = len(cart_data_before) - len(even_positions)
            assert (
                len(cart_data_after) == expected_items_after
            ), "Некорректное количество товаров в корзине после удаления"

            total_after = self.cart_page.get_total_price()
            assert (
                total_after is not None and total_after >= 0
            ), "Некорректная итоговая стоимость корзины после удаления"

            expected_total_after = total_before - removed_sum
            assert total_after == pytest.approx(
                expected_total_after, abs=0.01
            ), f"Итоговая стоимость после удаления должна быть {expected_total_after}, получено {total_after}"
