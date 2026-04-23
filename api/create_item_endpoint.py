from typing import Any, Dict
import allure
import logging

from api.base_endpoint import BaseEndpoint
from utils.api.api_validators import validate_create_item_response 


logger = logging.getLogger(__name__)

class CreateItemEndpoint(BaseEndpoint):
    """Эндпоинт для создания нового товара."""

    @allure.step("Создаем новый товар с данными: {item_data}")
    def action(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Создаем новый товар с данными: {item_data}")
        self.response = self.session.post(self.create_url, json=item_data)
        self.response_json = self.response.json()
        validate_create_item_response(self.response_json)
        return self.response_json
    
    @allure.step("Создание нового объекта с ошибкой (expecting error)")
    def action_expect_error(self, payload: Dict[str, Any], expected_code: int) -> Dict[str, Any]:
        """Создание нового объекта с ошибкой (expecting error)"""
        logger.info(f"Создаем новый товар с данными: {payload}, ожидая ошибку с кодом {expected_code}")
        self.response = self.session.post(
            self.create_url,
            json=payload,
        )
        self.response_json = self.response.json() if self.response.text else {}
        self.check_status_code(expected_code)
        return self.response_json