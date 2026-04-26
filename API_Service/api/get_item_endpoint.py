from typing import Any, Dict
import allure
import logging

from API_Service.api.base_endpoint import BaseEndpoint
from API_Service.schemas.ItemSchema import ItemResponseSchema
from utils.api.api_validators import validate_get_item_response

logger = logging.getLogger(__name__)

class GetItemEndpoint(BaseEndpoint):
    """Эндпоинт для получения товара по ID."""

    @allure.step("Получаем информацию о товаре с ID: {item_id}")
    def action(self, item_id: int) -> ItemResponseSchema:
        logger.info(f"Получаем информацию о товаре с ID: {item_id}")
        self.response = self.session.get(f"{self.get_by_id_url}{item_id}")
        self.response_json = self.response.json()
        return validate_get_item_response(self.response_json)
    
    @allure.step("Получаем информацию о товаре с ID: {item_id}, ожидая ошибку с кодом {expected_code}")
    def action_expect_error(self, item_id: int, expected_code: int) -> int:
        """Получаем информацию о товаре с ID: {item_id}, ожидая ошибку с кодом {expected_code}"""
        logger.info(f"Получаем информацию о товаре с ID: {item_id}, ожидая ошибку с кодом {expected_code}")
        self.response = self.session.get(f"{self.get_by_id_url}{item_id}")
        self.check_status_code(expected_code)
        return True