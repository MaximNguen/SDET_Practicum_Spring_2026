import allure
import logging

from clients.item_client import ItemClient
from utils.api.payloads import build_payload
from utils.api.api_validators import validate_get_item_response

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Get Item Endpoint")
@allure.feature("Get Item by ID")
class TestGetItemEndpoint:
    """Тесты для эндпоинта получения объекта по ID."""
    
    @allure.title("Успешное получение объекта по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка успешного получения объекта по ID.\n
        Предусловие - Создать новый объект через API и получить его ID.\n
        Шаги:\n
        1. Создать новый объект через API и получить его ID.\n
        2. Отправить запрос на получение объекта по ID.\n
        3. Проверить, что статус код ответа 200.\n
        4. Проверить, что данные объекта в ответе соответствуют данным, которые были
              отправлены при создании объекта.\n
        Ожидаемый результат - Объект успешно получен по ID, статус код 200, и данные объекта в ответе соответствуют данным при создании."""
    )
    def test_get_item_by_id_success(self, item_client: ItemClient):
        """Тест на успешное получение объекта по ID."""
        logger.info("Тест на успешное получение объекта по ID начинается.")
        payload = build_payload()
        item = item_client.create_item(payload)
        response_json = item_client.get_item_by_id(item)
        validate_get_item_response(response_json)
        status = item_client.get_status_code(item)
        
        assert status == 200, f"Ожидался статус код 200, но получен: {status}"
        assert response_json["title"] == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_json['title']}"
        assert response_json["verified"] == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_json['verified']}"
        assert response_json["important_numbers"] == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_json['important_numbers']}"
        assert response_json["addition"]["additional_info"] == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_json['addition']['additional_info']}"
        assert response_json["addition"]["additional_number"] == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_json['addition']['additional_number']}"
        assert response_json["id"] == response_json["addition"]["id"], f"Ожидалось совпадение ID: {response_json['id']} и ID в добавлении: {response_json['addition']['id']}, но получено: {response_json['addition']['id']}"
        
    @allure.title("Получение объекта по несуществующему ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка получения объекта по несуществующему ID.\n
        Предусловие - Убедиться, что ID, который будет использоваться для запроса, не существует в системе.\n
        Шаги:\n
        1. Отправить запрос на получение объекта по несуществующему ID.\n
        2. Проверить, что статус код ответа 500.\n
        3. Проверить, что в ответе содержится сообщение об ошибке или пустой объект.\n
        Ожидаемый результат - Получение ошибки с статус кодом 500 и соответствующим сообщением об ошибке или пустым объектом."""
    )
    def test_get_item_by_id_not_found(self, item_client: ItemClient):
        """Тест на получение объекта по несуществующему ID."""
        logger.info("Тест на получение объекта по несуществующему ID начинается.")
        non_existent_id = 999999
        response_json = item_client.get_item_by_id(non_existent_id)
        status = item_client.get_status_code(non_existent_id)
        
        assert status == 500, f"Ожидался статус код 500, но получен: {status}"
        assert response_json == {} or "error" in response_json, f"Ожидался пустой объект или сообщение об ошибке, но получено: {response_json}"