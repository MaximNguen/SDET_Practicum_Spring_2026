import allure
import logging

from API_Service.clients.item_client import ItemClient
from utils.api.payloads import build_payload
from utils.api.api_validators import validate_create_item_response

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Patch Item Endpoint")
@allure.feature("Patch Item by ID")
class TestPatchItemEndpoint:
    """Тесты для эндпоинта частичного обновления объекта по ID."""
    
    @allure.title("Успешное частичное обновление объекта по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка успешного частичного обновления объекта по ID.\n
        Шаги:\n
        1. Создать новый объект через API и получить его ID.\n
        2. Подготовить данные для частичного обновления (например, изменить только одно поле).\n
        3. Отправить запрос на частичное обновление объекта по ID с подготовленными данными.\n
        4. Проверить, что статус код ответа 200.\n
        5. Отправить запрос на получение объекта по тому же ID и убедиться, что измененное поле было обновлено, а остальные поля остались без изменений.\n
        Ожидаемый результат - Объект успешно частично обновлен по ID, статус код 200 при обновлении, и измененное поле было обновлено, а остальные поля остались без изменений при получении объекта.
        Постусловие - Удалить созданный объект, если он был успешно создан, чтобы поддерживать чистоту тестовой среды."""
    )
    def test_patch_item_by_id_success(self, item_client: ItemClient, item_clean_all):
        """Тест на успешное частичное обновление объекта по ID."""
        logger.info("Тест на успешное частичное обновление объекта по ID начинается.")
        payload = build_payload()
        validate_create_item_response(payload)
        item = item_client.create_item(payload)
        item_clean_all(item)
        response_model = item_client.get_item_by_id(item)
        
        assert response_model.title == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_model.title}"
        assert response_model.verified == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_model.verified}"
        assert response_model.important_numbers == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_model.important_numbers}"
        assert response_model.addition.additional_info == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_model.addition.additional_info}"
        assert response_model.addition.additional_number == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_model.addition.additional_number}"
        assert response_model.id == response_model.addition.id, f"Ожидалось совпадение ID: {response_model.id} и ID в добавлении: {response_model.addition.id}, но получено: {response_model.addition.id}"
        
        new_payload = build_payload()
        validate_create_item_response(new_payload)
        patch_response = item_client.update_item(item, new_payload)
        assert patch_response is True, f"Ожидался статус код 204 при частичном обновлении объекта, но получен: {patch_response}"
        
        get_response = item_client.get_item_by_id(item)
        assert get_response.title == new_payload["title"], f"Ожидалось имя: {new_payload['title']}, но получено: {get_response.title}"
        assert get_response.verified == new_payload["verified"], f"Ожидался статус: {new_payload['verified']}, но получен: {get_response.verified}"
        assert get_response.important_numbers == new_payload["important_numbers"], f"Ожидались числа: {new_payload['important_numbers']}, но получены: {get_response.important_numbers}"
        assert get_response.addition.additional_info == new_payload["addition"]["additional_info"], f"Ожидалось добавление: {new_payload['addition']['additional_info']}, но получено: {get_response.addition.additional_info}"
        assert get_response.addition.additional_number == new_payload["addition"]["additional_number"], f"Ожидалось добавление: {new_payload['addition']['additional_number']}, но получено: {get_response.addition.additional_number}"