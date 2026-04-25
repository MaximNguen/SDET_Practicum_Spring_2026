from typing import Any, Dict, List
import allure
import logging

from API_Service.api.base_endpoint import BaseEndpoint
from utils.api.api_validators import validate_create_item_response
from API_Service.clients.item_client import ItemClient

logger = logging.getLogger(__name__)

class UpdateItemEndpoint(BaseEndpoint):
    """Эндпоинт для обновления товара по ID."""

    @allure.step("Обновляем товар с ID: {item_id} данными: {item_data}")
    def action(self, item_id: int, item_data: Dict[str, Any]) -> bool:
        logger.info(f"Обновляем товар с ID: {item_id} данными: {item_data}")
        self.response = self.session.patch(f"{self.patch_url}{item_id}", json=item_data)
        self.check_status_code(204)
        return True
    
    @allure.step("Обновляем товар с ID: {item_id} данными: {item_data}, ожидая ошибку с кодом {expected_code}")
    def action_expect_error(self, item_id: int, item_data: Dict[str, Any], expected_code: int) -> bool:
        """Обновляем товар с ID: {item_id} данными: {item_data}, ожидая ошибку с кодом {expected_code}"""
        logger.info(f"Обновляем товар с ID: {item_id} данными: {item_data}, ожидая ошибку с кодом {expected_code}")
        self.response = self.session.patch(f"{self.patch_url}{item_id}", json=item_data)
        self.check_status_code(expected_code)
        return True