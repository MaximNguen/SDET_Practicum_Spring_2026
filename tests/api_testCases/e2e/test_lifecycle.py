import allure
import logging

from clients.item_client import ItemClient
from utils.api.api_validators import validate_get_item_response, validate_create_item_response
from utils.api.payloads import build_payload

logger = logging.getLogger(__name__)

@allure.epic("API Tests - Item Lifecycle")
@allure.feature("Item Lifecycle")
class TestItemLifecycle:
    """Тесты для проверки полного жизненного цикла объекта."""
    
    @allure.title("Проверка полного жизненного цикла объекта")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        """Проверка полного жизненного цикла объекта - создание, получение, обновление и удаление.\n
        Шаги:\n
        1. Создать новый объект через API и получить его ID.\n
        2. Отправить запрос на получение объекта по ID и проверить, что данные соответствуют данным при создании.\n
        3. Подготовить данные для частичного обновления объекта и отправить запрос на обновление по ID.\n
        4. Отправить запрос на получение объекта по тому же ID и проверить, что измененное поле было обновлено, а остальные поля остались без изменений.\n
        5. Отправить запрос на удаление объекта по ID.\n
        6. Отправить запрос на получение объекта по тому же ID и убедиться, что он больше не существует (статус код 500 или соответствующее сообщение об ошибке).\n
        Ожидаемый результат - Объект успешно проходит полный жизненный цикл: создается, данные при получении соответствуют данным при создании, успешно обновляется, а затем удаляется и больше не существует при попытке его получения."""
    )
    def test_item_lifecycle(self, item_client: ItemClient):
        """Тест на проверку полного жизненного цикла объекта."""
        logger.info("Тест на проверку полного жизненного цикла объекта начинается.")
        payload = build_payload()
        validate_create_item_response(payload)
        item = item_client.create_item(payload)
        logger.info(f"Новый объект успешно создан - {item} и получен по ID.")
        
        response_json = item_client.get_item_by_id(item)
        validate_get_item_response(response_json)
        
        assert response_json["title"] == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_json['title']}"
        assert response_json["verified"] == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_json['verified']}"
        assert response_json["important_numbers"] == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_json['important_numbers']}"
        assert response_json["addition"]["additional_info"] == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_json['addition']['additional_info']}"
        assert response_json["addition"]["additional_number"] == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_json['addition']['additional_number']}"
        assert response_json["id"] == response_json["addition"]["id"], f"Ожидалось совпадение ID: {response_json['id']} и ID в добавлении: {response_json['addition']['id']}, но получено: {response_json['addition']['id']}"
        
        new_payload = build_payload()
        validate_create_item_response(new_payload)
        patch_response = item_client.update_item(item, new_payload)
        assert patch_response == 204, f"Ожидался статус код 204 при частичном обновлении объекта, но получен: {patch_response}"
        
        response_json_updated = item_client.get_item_by_id(item)
        validate_get_item_response(response_json_updated)
        assert response_json_updated["title"] == new_payload["title"], f"Ожидалось имя: {new_payload['title']}, но получено: {response_json_updated['title']}"
        assert response_json_updated["verified"] == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_json_updated['verified']}"
        assert response_json_updated["important_numbers"] == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_json_updated['important_numbers']}"
        assert response_json_updated["addition"]["additional_info"] == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_json_updated['addition']['additional_info']}"
        assert response_json_updated["addition"]["additional_number"] == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_json_updated['addition']['additional_number']}"
        assert response_json_updated["id"] == response_json_updated["addition"]["id"], f"Ожидалось совпадение ID: {response_json_updated['id']} и ID в добавлении: {response_json_updated['addition']['id']}, но получено: {response_json_updated['addition']['id']}"
        
        delete_response = item_client.delete_item(item)
        assert delete_response == 204, f"Ожидался статус код 204 при удалении объекта, но получен: {delete_response}"
        
        get_response_after_delete = item_client.get_item_by_id_after_delete(item)
        assert get_response_after_delete == 500, f"Ожидался статус код 500 при попытке получения удаленного объекта, но получен: {get_response_after_delete}"