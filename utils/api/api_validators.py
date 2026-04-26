from typing import Any, Mapping
from pydantic import BaseModel, ValidationError
import allure
import logging

logger = logging.getLogger(__name__)

from API_Service.schemas.ItemSchema import ItemResponseSchema, ItemRequestSchema, ItemsListResponseSchema, ResponseCreatedSchema


def extract_item_id_from_create_response(response_json: Mapping[str, Any]) -> int:
    """Извлекает ID товара из ответа при его создании."""
    with allure.step("Извлекаем ID товара из ответа при его создании"):
        try:
            logger.info(f"Извлекаем ID из ответа: {response_json}, используя схему ItemResponseSchema")
            item_response = ItemResponseSchema.from_dict(response_json)
            return item_response.id
        except Exception as e:
            logger.error(f"Не удалось извлечь ID из ответа: {e}")
            raise ValueError(f"Не удалось извлечь ID из ответа: {e}")
    
def validate_create_item_response(response_json: Mapping[str, Any]) -> ItemRequestSchema:
    """Проверяет, что ответ при создании товара соответствует схеме ItemRequestSchema."""
    with allure.step("Проверяем, что ответ при создании товара соответствует схеме ItemRequestSchema"):
        logger.info(f"Проверяем ответ при создании товара: {response_json}, используя схему ItemRequestSchema")
        try:
            return ItemRequestSchema.from_dict(response_json)
        except Exception as e:
            logger.error(f"Ошибка валидации ответа при создании товара: {e}")
            raise ValueError(f"Ответ не соответствует схеме ItemRequestSchema: {e}")

def validate_get_item_response(response_json: Mapping[str, Any]) -> ItemResponseSchema:
    """Проверяет, что ответ при получении товара соответствует схеме ItemResponseSchema."""
    with allure.step("Проверяем, что ответ при получении товара соответствует схеме ItemResponseSchema"):   
        logger.info(f"Проверяем ответ при получении товара: {response_json}, используя схему ItemResponseSchema")
        try:
            return ItemResponseSchema.from_dict(response_json)
        except Exception as e:
            logger.error(f"Ошибка валидации ответа при получении товара: {e}")
            raise ValueError(f"Ответ не соответствует схеме ItemResponseSchema: {e}")

def validate_get_all_items_response(response_json: Mapping[str, Any]) -> ItemsListResponseSchema:
    """Проверяет, что ответ при получении всех товаров соответствует схеме ItemsListResponseSchema."""
    with allure.step("Проверяем, что ответ при получении всех товаров соответствует схеме ItemsListResponseSchema"):
        logger.info(f"Проверяем ответ при получении всех товаров: {response_json}, используя схему ItemsListResponseSchema")
        try:
            return ItemsListResponseSchema.from_dict(response_json)
        except ValidationError as e:
            logger.error(f"Ошибка валидации ответа при получении всех товаров: {e}")
            raise ValueError(f"Ответ не соответствует схеме ItemsListResponseSchema: {e}")
        except Exception as e:
            logger.error(f"Ошибка при валидации списка объектов: {e}")
            raise ValueError(f"Ошибка при валидации списка объектов: {e}")
        
def validate_id_item_response(response_json: Mapping[str, Any]) -> ResponseCreatedSchema:
    """Проверяет, что ответ при создании товара соответствует схеме ResponseCreatedSchema."""
    with allure.step("Проверяем, что ответ при получении товара соответствует схеме ResponseCreatedSchema"):   
        logger.info(f"Проверяем ответ при получении товара: {response_json}, используя схему ResponseCreatedSchema")
        try:
            return ResponseCreatedSchema(id=int(response_json))
        except Exception as e:
            logger.error(f"Ошибка валидации ответа при получении товара: {e}")
            raise ValueError(f"Ответ не соответствует схеме ResponseCreatedSchema: {e}")