from typing import Any, Mapping, cast
from pydantic import TypeAdapter
import allure
import logging

logger = logging.getLogger(__name__)

from schemas.ItemSchema import ItemResponseSchema, ItemRequestSchema

def extract_item_id_from_create_response(response_json: Mapping[str, Any]) -> int:
    """Извлекает ID товара из ответа при его создании."""
    with allure.step("Извлекаем ID товара из ответа при его создании"):
        try:
            logger.info(f"Извлекаем ID из ответа: {response_json}, используя схему ItemResponseSchema")
            item_response = TypeAdapter(ItemResponseSchema).validate_python(response_json)
            return item_response.id
        except Exception as e:
            raise ValueError(f"Не удалось извлечь ID из ответа: {e}")
    
def validate_create_item_response(response_json: Mapping[str, Any]) -> ItemRequestSchema:
    """Проверяет, что ответ при создании товара соответствует схеме ItemRequestSchema."""
    with allure.step("Проверяем, что ответ при создании товара соответствует схеме ItemRequestSchema"):
        logger.info(f"Проверяем ответ при создании товара: {response_json}, используя схему ItemRequestSchema")
        try:
            return TypeAdapter(ItemRequestSchema).validate_python(response_json)
        except Exception as e:
            raise ValueError(f"Ответ не соответствует схеме ItemRequestSchema: {e}")
    
def validate_get_item_response(response_json: Mapping[str, Any]) -> ItemResponseSchema:
    """Проверяет, что ответ при получении товара соответствует схеме ItemResponseSchema."""
    with allure.step("Проверяем, что ответ при получении товара соответствует схеме ItemResponseSchema"):   
        logger.info(f"Проверяем ответ при получении товара: {response_json}, используя схему ItemResponseSchema")
        try:
            return TypeAdapter(ItemResponseSchema).validate_python(response_json)
        except Exception as e:
            raise ValueError(f"Ответ не соответствует схеме ItemResponseSchema: {e}")