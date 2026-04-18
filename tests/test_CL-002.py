import allure
import pytest
import random

from data.urls import main_page_url
from data.mock_data import search_value

@allure.epic("Выполнение Чек-листа 002 - Проверка добавления товара в корзину, поиск товаров и изменение корзины")
@allure.feature("Тест-кейсы для проверки добавления товара в корзину, поиск товаров и изменение корзины")
class TestSearchAndCartFunctionality:
    """Тест-кейсы для проверки добавления товара в корзину, поиск товаров и изменение корзины."""

    @classmethod
    def setup_class(cls):
        print("\n========= Начало выполнения тест-кейсов на добавление товара в корзину, поиск товаров и изменение корзины ==========")

    @classmethod
    def teardown_class(cls):
        print("\n========= Конец выполнения тест-кейсов на добавление товара в корзину, поиск товаров и изменение корзины ==========")

    @pytest.fixture(autouse=True)
    def setup(self, main_page, items_page, product_page, cart_page, search_page, url=main_page_url):
        self.main_page = main_page
        self.items_page = items_page
        self.product_page = product_page
        self.cart_page = cart_page
        self.search_page = search_page
        self.main_page.open(url)
        yield self.main_page
        self.main_page.quit()
        
    @allure.story("Проверка наличия поля для ввода поиска на главной странице")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_search_input(self):
        """Проверка наличия поля для ввода поиска на главной странице."""
        search_input = self.main_page.get_search_input()
        assert search_input.is_displayed(), f"Не отображается поле ввода поиска на главной странице"
        
    @allure.story("Проверка результатов поиска после ввода текста")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_search_results(self):
        """Проверка результатов поиска после ввода текста."""
        search_input = self.main_page.get_search_input()
        with allure.step(f"Вводим текст '{search_value}' в поле поиска и проверяем результаты"):
            self.main_page.enter_search_value(search_input)
            results = self.search_page.get_products_cards()
            assert results, f"По запросу '{search_value}' не найдено товаров."
            
    @allure.story("Проверка наличия товаров в корзине после добавления")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_add_to_cart_button(self):
        """Проверка наличия товаров в корзине после добавления."""
        search_input = self.main_page.get_search_input()
        with allure.step(f"Вводим текст '{search_value}' в поле поиска"):
            self.main_page.enter_search_value(search_input)
            cards = self.search_page.get_products_current_items([2, 3])
            
            assert len(cards) == 2, f"Не найдены карточки товаров для добавления в корзину."
            
        for card in cards:
            with allure.step("Переходим на страницу товара и проверяем наличие кнопки добавления товара в корзину"):
                self.search_page.click_add_cart_button(card)
                input_quantity = self.product_page.get_input_quantity()
                
                assert input_quantity.is_displayed(), f"Не отображается поле ввода количества товара на странице товара"
                
                with allure.step("Устанавливаем случайное количество товара и кликаем по кнопке добавления товара в корзину"):
                    self.product_page.set_random_quantity()
                    self.product_page.click_add_to_cart_button()
                    self.wait.wait_for_page_load()
                    self.main_page.go_back_page()
                    self.main_page.go_back_page()
                    
        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, f"В корзине не найдено товаров после добавления."
        
    @allure.story("Проверка изменения товаров в корзине после добавления")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_quantity_for_lowest(self):
        """Проверка изменения товаров в корзине после добавления."""
        search_input = self.main_page.get_search_input()
        with allure.step(f"Вводим текст '{search_value}' в поле поиска"):
            self.main_page.enter_search_value(search_input)
            cards = self.search_page.get_products_current_items([2, 3])
            
            assert len(cards) == 2, f"Не найдены карточки товаров для добавления в корзину."
            
        for card in cards:
            with allure.step("Переходим на страницу товара и проверяем наличие кнопки добавления товара в корзину"):
                self.search_page.click_add_cart_button(card)
                input_quantity = self.product_page.get_input_quantity()
                
                assert input_quantity.is_displayed(), f"Не отображается поле ввода количества товара на странице товара"
                
                with allure.step("Устанавливаем случайное количество товара и кликаем по кнопке добавления товара в корзину"):
                    self.product_page.set_random_quantity()
                    self.product_page.click_add_to_cart_button()
                    self.main_page.go_back_page()
                    self.main_page.go_back_page()
                    
        self.main_page.go_to_cart_page()
        cart_items = self.cart_page.get_cart_items_data()
        assert len(cart_items) == 2, f"В корзине не найдено товаров после добавления."
        
        total_price = self.cart_page.get_total_price()
        assert total_price > 0, f"Общая стоимость товаров в корзине не отображается или равна нулю."
        
        lowest_data = self.cart_page.get_lowest_price_item()
        self.cart_page.double_quantity_lowest_price_item()
        new_total_price = self.cart_page.get_total_price()
        
        assert new_total_price > total_price, f"Общая стоимость товаров в корзине не изменилась после изменения количества товара с самой низкой ценой."
        
        new_data = lowest_data['quantity'] * lowest_data['price']
        assert new_total_price == total_price + new_data, f"Общая стоимость товаров в корзине не изменилась на сумму удвоенного количества товара с самой низкой ценой."