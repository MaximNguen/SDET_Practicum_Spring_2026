from typing import Any, Dict
import logging
import allure

from API_Service.clients.base_client import BaseClient
from config import CREATE_URL, DELETE_URL, GET_ALL_URL, GET_BY_ID_URL, PATCH_URL
from API_Service.schemas.ItemSchema import ItemResponseSchema, ItemsListResponseSchema
from utils.api.api_validators import validate_get_all_items_response, validate_get_item_response

logger = logging.getLogger(__name__)

class ItemClient(BaseClient):
    """Клиент для взаимодействия с API товаров."""

    @allure.step("Создаем новый товар с данными: {item_data}")
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание нового товара."""
        logger.info(f"Создаем новый товар с данными: {item_data}")
        response = self.send_request("POST", CREATE_URL, json=item_data)
        return response.json()

    @allure.step("Удаляем товар с ID: {item_id}")
    def delete_item(self, item_id: int) -> int:
        """Удаление товара по ID."""
        logger.info(f"Удаляем товар с ID: {item_id}")
        response = self.send_request("DELETE", f"{DELETE_URL}{item_id}")
        return response.status_code

    @allure.step("Получаем список всех товаров")
    def get_all_items(self) -> ItemsListResponseSchema:
        """Получение списка всех товаров."""
        logger.info("Получаем список всех товаров.")
        response = self.send_request("GET", GET_ALL_URL)
        return validate_get_all_items_response(response.json())

    @allure.step("Получаем информацию о товаре с ID: {item_id}")
    def get_item_by_id(self, item_id: int) -> ItemResponseSchema:
        """Получение товара по ID."""
        logger.info(f"Получаем информацию о товаре с ID: {item_id}")
        response = self.send_request("GET", f"{GET_BY_ID_URL}{item_id}")
        return validate_get_item_response(response.json())
    
    @allure.step("Получаем информацию о товаре с ID: {item_id}")
    def get_item_by_id_after_delete(self, item_id: int) -> Dict[str, Any]:
        """Получение товара по ID."""
        logger.info(f"Получаем информацию о товаре с ID: {item_id}")
        response = self.send_request("GET", f"{GET_BY_ID_URL}{item_id}")
        return response.status_code

    @allure.step("Обновляем информацию о товаре с ID: {item_id} данными: {update_data}")
    def update_item(self, item_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление товара по ID."""
        logger.info(f"Обновляем информацию о товаре с ID: {item_id}")
        response = self.send_request("PATCH", f"{PATCH_URL}{item_id}", json=update_data)
        return response.status_code
    
    @allure.step("Получить информацию о статус коде")
    def get_status_code(self, item_id: int) -> int:
        """Получение статус кода для товара по ID."""
        logger.info(f"Получаем информацию о статус коде для товара с ID: {item_id}")
        response = self.send_request("GET", f"{GET_BY_ID_URL}{item_id}")
        return response.status_code