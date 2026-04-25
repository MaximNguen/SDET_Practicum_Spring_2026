from typing import Any, Dict
import allure
import logging

from API_Service.api.base_endpoint import BaseEndpoint
from API_Service.schemas.ItemSchema import ResponseCreatedSchema
from utils.api.api_validators import validate_create_item_response, validate_id_item_response


logger = logging.getLogger(__name__)

class CreateItemEndpoint(BaseEndpoint):
    """Эндпоинт для создания нового товара."""

    @allure.step("Создаем новый товар с данными: {item_data}")
    def action(self, item_data: Dict[str, Any]) -> ResponseCreatedSchema:
        validate_create_item_response(item_data)
        logger.info(f"Создаем новый товар с данными: {item_data}")
        self.response = self.session.post(self.create_url, json=item_data)
        self.response_json = self.response.json()
        return validate_id_item_response(self.response_json)
    
    @allure.step("Создание нового объекта с ошибкой (expecting error)")
    def action_expect_error(self, payload: Dict[str, Any], expected_code: int) -> bool:
        """Создание нового объекта с ошибкой (expecting error)"""
        logger.info(f"Создаем новый товар с данными: {payload}, ожидая ошибку с кодом {expected_code}")
        self.response = self.session.post(
            self.create_url,
            json=payload,
        )
        self.response_json = self.response.json() if self.response.text else {}
        return self.check_status_code(expected_code)