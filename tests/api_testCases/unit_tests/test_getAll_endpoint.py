import allure
import logging

from clients.item_client import ItemClient
from conftest import item_client
from utils.api.api_validators import validate_get_item_response, validate_create_item_response
from utils.api.payloads import build_payload

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Get All Items Endpoint")
@allure.feature("Get All Items")
class TestGetAllItemsEndpoint:
    """Тесты для эндпоинта получения всех объектов."""

    @allure.title("Успешное получение списка всех объектов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка успешного получения списка всех объектов.\n
        Предусловие - Создать несколько объектов через API для обеспечения наличия данных в системе.\n
        Шаги:\n
        1. Создать несколько объектов через API для обеспечения наличия данных в системе.\n
        2. Отправить запрос на получение списка всех объектов.\n
        3. Проверить, что статус код ответа 200.\n
        4. Проверить, что ответ содержит список объектов и что каждый объект соответствует ожидаемой структуре данных.\n
        Ожидаемый результат - Список всех объектов успешно получен, статус код 200, и каждый объект соответствует ожидаемой структуре данных."""
    )
    def test_get_all_items_success(self, item_client: ItemClient):
        """Тест на успешное получение списка всех объектов."""
        logger.info("Тест на успешное получение списка всех объектов начинается.")
        items = []
        response_json_before = item_client.get_all_items()
        for _ in range(3):
            logger.info("Создаем новый объект для обеспечения наличия данных в системе.")
            builed_payload = build_payload()
            validate_create_item_response(builed_payload)
            item = item_client.create_item(builed_payload)
            get_item_response = item_client.get_item_by_id(item)
            validate_get_item_response(get_item_response)
            logger.info(f"Новый объект успешно создан - {get_item_response} и получен по ID, добавляем его в список для проверки общего количества объектов.")
            items.append(get_item_response)
            
            status = item_client.get_status_code(item)
            assert status == 200, f"Ожидался статус код 200 при создании объекта, но получен: {status}"
        
        response_json = item_client.get_all_items()
        assert isinstance(response_json, dict), f"Ожидался список, но получен: {type(response_json)}"
        assert len(response_json_before["entity"]) + 3 == len(response_json["entity"]), f"Ожидалось количество объектов: {len(response_json_before['entity']) + 3}, но получено: {len(response_json['entity'])}"