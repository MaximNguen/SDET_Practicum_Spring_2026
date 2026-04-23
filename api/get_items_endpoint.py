from typing import Any, Dict
import allure
import logging

from api.base_endpoint import BaseEndpoint
from utils.api.api_validators import validate_get_all_items_response

logger = logging.getLogger(__name__)

class GetAllItemsEndpoint(BaseEndpoint):
    """Эндпоинт для получения всех товаров."""

    @allure.step("Получаем список всех товаров")
    def action(self) -> list[Dict[str, Any]]:
        logger.info("Получаем список всех товаров")
        self.response = self.session.get(self.get_all_url)
        self.response_json = self.response.json()
        return validate_get_all_items_response(self.response_json)