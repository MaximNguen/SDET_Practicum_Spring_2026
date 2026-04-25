import allure
import logging

from API_Service.api.factory_endpoint.factory_endpoint import FactoryEndpoint
from utils.api.api_validators import validate_create_item_response
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
        Ожидаемый результат - Объект успешно проходит полный жизненный цикл: создается, данные при получении соответствуют данным при создании, успешно обновляется, а затем удаляется и больше не существует при попытке его получения.
        Постусловие - Удалить созданный объект, если он был успешно создан, чтобы поддерживать чистоту тестовой среды."""
    )
    def test_item_lifecycle(self, endpoint_factory: FactoryEndpoint, item_clean_all):
        """Тест на проверку полного жизненного цикла объекта."""
        logger.info("Тест на проверку полного жизненного цикла объекта начинается.")

        create_endpoint = endpoint_factory.get("create")
        get_endpoint = endpoint_factory.get("get")
        patch_endpoint = endpoint_factory.get("patch")
        delete_endpoint = endpoint_factory.get("delete")

        payload = build_payload()
        validate_create_item_response(payload)
        item_id = create_endpoint.action(payload)
        item_clean_all(item_id)
        logger.info("Новый объект успешно создан и получен по ID: %s", item_id)
        
        response_model = get_endpoint.action(item_id)
        
        assert response_model.title == payload["title"], f"Ожидалось имя: {payload['title']}, но получено: {response_model.title}"
        assert response_model.verified == payload["verified"], f"Ожидался статус: {payload['verified']}, но получен: {response_model.verified}"
        assert response_model.important_numbers == payload["important_numbers"], f"Ожидались числа: {payload['important_numbers']}, но получены: {response_model.important_numbers}"
        assert response_model.addition.additional_info == payload["addition"]["additional_info"], f"Ожидалось добавление: {payload['addition']['additional_info']}, но получено: {response_model.addition.additional_info}"
        assert response_model.addition.additional_number == payload["addition"]["additional_number"], f"Ожидалось добавление: {payload['addition']['additional_number']}, но получено: {response_model.addition.additional_number}"
        assert response_model.id == response_model.addition.id, f"Ожидалось совпадение ID: {response_model.id} и ID в добавлении: {response_model.addition.id}, но получено: {response_model.addition.id}"
        
        new_payload = build_payload()
        validate_create_item_response(new_payload)
        patch_response = patch_endpoint.action(item_id, new_payload)
        assert patch_response is True, f"Ожидался статус код 204 при частичном обновлении объекта, но получен: {patch_response}"
        
        response_model_updated = get_endpoint.action(item_id)
        assert response_model_updated.title == new_payload["title"], f"Ожидалось имя: {new_payload['title']}, но получено: {response_model_updated.title}"
        assert response_model_updated.verified == new_payload["verified"], f"Ожидался статус: {new_payload['verified']}, но получен: {response_model_updated.verified}"
        assert response_model_updated.important_numbers == new_payload["important_numbers"], f"Ожидались числа: {new_payload['important_numbers']}, но получены: {response_model_updated.important_numbers}"
        assert response_model_updated.addition.additional_info == new_payload["addition"]["additional_info"], f"Ожидалось добавление: {new_payload['addition']['additional_info']}, но получено: {response_model_updated.addition.additional_info}"
        assert response_model_updated.addition.additional_number == new_payload["addition"]["additional_number"], f"Ожидалось добавление: {new_payload['addition']['additional_number']}, но получено: {response_model_updated.addition.additional_number}"
        assert response_model_updated.id == response_model_updated.addition.id, f"Ожидалось совпадение ID: {response_model_updated.id} и ID в добавлении: {response_model_updated.addition.id}, но получено: {response_model_updated.addition.id}"
        
        delete_response = delete_endpoint.action(item_id)
        assert delete_response is True, f"Ожидался статус код 204 при удалении объекта, но получен: {delete_response}"
        
        get_response_after_delete = get_endpoint.action_expect_error(item_id, expected_code=500)
        assert get_response_after_delete is True, (
            f"Ожидался статус код 500 при запросе после удаления, но получен: {get_response_after_delete}"
        )