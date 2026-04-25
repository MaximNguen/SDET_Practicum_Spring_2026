import allure
import logging

from API_Service.clients.item_client import ItemClient
from utils.api.payloads import build_payload
from utils.api.api_validators import validate_create_item_response

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Delete Item Endpoint")
@allure.feature("Delete Item by ID")
class TestDeleteItemEndpoint:
    """Тесты для эндпоинта удаления объекта."""
    
    @allure.title("Успешное удаление объекта по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка успешного удаления объекта по ID.\n
        Шаги:\n
        1. Создать новый объект через API и получить его ID.\n
        2. Отправить запрос на удаление объекта по ID.\n
        3. Проверить, что статус код ответа 204.\n
        4. Отправить запрос на получение объекта по тому же ID и убедиться, что он больше не существует (статус код 404 или соответствующее сообщение об ошибке).\n
        Ожидаемый результат - Объект успешно удален по ID, статус код 204 при удалении, и объект больше не существует при попытке его получения.
        Постусловие - Удалить созданный объект, если он был успешно создан, чтобы поддерживать чистоту тестовой среды."""
    )
    def test_delete_item_by_id_success(self, item_client: ItemClient, item_clean_all):
        """Тест на успешное удаление объекта по ID."""
        logger.info("Тест на успешное удаление объекта по ID начинается.")
        payload = build_payload()
        validate_create_item_response(payload)
        item = item_client.create_item(payload)
        item_clean_all(item.id)
        delete_response = item_client.delete_item(item.id)
        
        assert delete_response is True, f"Ожидался статус код 204 при удалении объекта, но получен: {delete_response}"
        
        get_response = item_client.get_item_by_id_after_delete(item)
        assert get_response is False, f"Ожидался статус код 404 при попытке получения удаленного объекта, но получен: {get_response}"