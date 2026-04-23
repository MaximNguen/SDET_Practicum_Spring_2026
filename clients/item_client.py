from typing import Any, Dict
import logging

from clients.base_client import BaseClient
from config import CREATE_URL, DELETE_URL, GET_ALL_URL, GET_BY_ID_URL, PATCH_URL

logger = logging.getLogger(__name__)

class ItemClient(BaseClient):
    """Клиент для взаимодействия с API товаров."""

    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание нового товара."""
        response = self.send_request("POST", CREATE_URL, json=item_data)
        return response.json()

    def delete_item(self, item_id: int) -> Dict[str, Any]:
        """Удаление товара по ID."""
        response = self.send_request("DELETE", f"{DELETE_URL}{item_id}")
        return response.json()

    def get_all_items(self) -> Dict[str, Any]:
        """Получение списка всех товаров."""
        response = self.send_request("GET", GET_ALL_URL)
        return response.json()

    def get_item_by_id(self, item_id: int) -> Dict[str, Any]:
        """Получение товара по ID."""
        response = self.send_request("GET", f"{GET_BY_ID_URL}{item_id}")
        return response.json()

    def update_item(self, item_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление товара по ID."""
        response = self.send_request("PATCH", f"{PATCH_URL}{item_id}", json=update_data)
        return response.json()