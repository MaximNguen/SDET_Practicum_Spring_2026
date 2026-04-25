import allure
import logging

from API_Service.clients.item_client import ItemClient
from utils.api.payloads import build_payload
from utils.api.api_validators import validate_create_item_response

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Create Item Endpoint")
@allure.feature("Create Item")
class TestCreateItemEndpoint:
    """Тесты для эндпоинта создания объекта."""
    
    @allure.title("Успешное создание нового объекта")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка успешного создания нового объекта.\n
        Шаги:\n
        1. Подготовить валидные данные для создания нового объекта.\n
        2. Отправить запрос на создание нового объекта с подготовленными данными.\n
        3. Проверить, что статус код ответа 200.\n
        4. Проверить, что данные в ответе соответствуют данным, которые были отправлены при создании объекта, и что в ответе присутствует уникальный идентификатор (ID) для нового объекта.\n
        Ожидаемый результат - Новый объект успешно создан, статус код 200, и данные в ответе соответствуют данным при создании объекта, включая наличие уникального идентификатора (ID)."""
    )
    def test_create_item_success(self, item_client: ItemClient, item_clean_all):
        logger.info("Тест на успешное создание нового объекта начинается.")
        payload = build_payload()
        validate_create_item_response(payload)
        item = item_client.create_item(payload)
        logger.info(f"Новый объект успешно создан - {item} и получен по ID.")
        response_model = item_client.get_item_by_id(item)
        item_clean_all(item)
        status = item_client.get_status_code(item)
        logger.info(f"Проверяем статус код ответа при получении объекта по ID - {status}.")
        
        assert status == 200, f"Ожидался статус код 200, но получен: {status}"
        assert response_model.title == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_model.title}"
        assert response_model.verified == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_model.verified}"
        assert response_model.important_numbers == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_model.important_numbers}"
        assert response_model.addition.additional_info == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_model.addition.additional_info}"
        assert response_model.addition.additional_number == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_model.addition.additional_number}"
        assert response_model.id == response_model.addition.id, f"Ожидалось совпадение ID: {response_model.id} и ID в добавлении: {response_model.addition.id}, но получено: {response_model.addition.id}"