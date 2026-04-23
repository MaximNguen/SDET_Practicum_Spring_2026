import allure
import logging

from clients.item_client import ItemClient
from utils.api.payloads import build_payload
from utils.api.api_validators import validate_get_item_response

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Get Item Endpoint")
@allure.feature("Get Item by ID")
class TestGetItemEndpoint:
    """Тесты для эндпоинта получения товара по ID."""
    
    @allure.story("Успешное получение товара по ID")
    def test_get_item_by_id_success(self, item_client: ItemClient):
        """Тест на успешное получение товара по ID."""
        logger.info("Тест на успешное получение товара по ID начинается.")
        payload = build_payload()
        item = item_client.create_item(payload)
        response_json = item_client.get_item_by_id(item)
        validate_get_item_response(response_json)
        
        assert response_json["title"] == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_json['title']}"
        assert response_json["verified"] == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_json['verified']}"
        assert response_json["important_numbers"] == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_json['important_numbers']}"
        assert response_json["addition"]["additional_info"] == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_json['addition']['additional_info']}"
        assert response_json["addition"]["additional_number"] == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_json['addition']['additional_number']}"
        assert response_json["id"] == response_json["addition"]["id"], f"Ожидалось совпадение ID: {response_json['id']} и ID в добавлении: {response_json['addition']['id']}, но получено: {response_json['addition']['id']}"