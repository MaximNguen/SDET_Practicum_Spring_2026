from __future__ import annotations

from typing import Any, Dict, List, Mapping, Type, TypeVar
import logging
import allure
from pydantic import BaseModel, ConfigDict, Field, field_validator

logger = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound="SchemaModelMixin")


class SchemaModelMixin(BaseModel):
    """Базовый миксин для явной сериализации/десериализации моделей."""

    @classmethod
    def from_dict(cls: Type[TModel], data: Mapping[str, Any]) -> TModel:
        return cls.model_validate(dict(data))

    @classmethod
    def from_json(cls: Type[TModel], data: str | bytes | bytearray) -> TModel:
        return cls.model_validate_json(data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="python")

    def to_json(self) -> str:
        return self.model_dump_json()

class ResponseCreatedSchema(SchemaModelMixin):
    """Схема для ответа при успешном создании объекта."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    id: int = Field(..., description="Уникальный идентификатор созданного объекта", ge=0)

class AdditionResponseSchema(SchemaModelMixin):
    """Схема для поля addition в ответе."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    id: int = Field(..., description="Уникальный идентификатор дополнительных данных", ge=0)
    additional_info: str = Field(..., description="Дополнительная информация", min_length=1)
    additional_number: int = Field(..., description="Дополнительное число", ge=0)
    
class ItemsListResponseSchema(SchemaModelMixin):
    """Схема для ответа со списком объектов."""
    entity: List[ItemResponseSchema] = Field(..., description="Список объектов")
    
class AdditionRequestSchema(SchemaModelMixin):
    """Схема для поля addition."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    additional_info: str = Field(..., description="Дополнительная информация", min_length=1)
    additional_number: int = Field(..., description="Дополнительное число", ge=0)

class ItemRequestSchema(SchemaModelMixin):
    """Схема для создания и обновления товара."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    addition: AdditionRequestSchema = Field(..., description="Дополнительные данные товара")
    important_numbers: List[int] = Field(..., description="Важные числа")
    title: str = Field(..., description="Название объекта", min_length=1)
    verified: bool = Field(..., description="Проверено ли")
    
    @field_validator("important_numbers")
    @classmethod
    @allure.step("Проверяем, что список важных чисел не пустой")
    def validate_important_numbers(cls, v: List[int]) -> List[int]:
        if not v:
            logger.error("Список важных чисел не может быть пустым")
            raise ValueError("Список важных чисел не может быть пустым")
        return v

    @field_validator("title")
    @classmethod
    @allure.step("Проверяем, что название объекта не пустое и не состоит только из пробелов")
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            logger.error("Название объекта не может быть пустым или состоять только из пробелов")
            raise ValueError("Название объекта не может быть пустым или состоять только из пробелов")
        return v
    
    @field_validator("addition")
    @classmethod
    @allure.step("Проверяем, что дополнительные данные не пустые")
    def validate_addition(cls, v: AdditionRequestSchema) -> AdditionRequestSchema:
        if not v.additional_info.strip():
            logger.error("Дополнительная информация не может быть пустой или состоять только из пробелов")
            raise ValueError("Дополнительная информация не может быть пустой или состоять только из пробелов")
        if len(str(v.additional_number)) == 0:
            logger.error("Дополнительное число не может быть пустым")
            raise ValueError("Дополнительное число не может быть пустым")
        return v
    
class ItemResponseSchema(SchemaModelMixin):
    """Схема для ответа при получении товара."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    id: int = Field(..., description="Уникальный идентификатор товара", ge=0)
    title: str = Field(..., description="Название объекта", min_length=1)
    verified: bool = Field(..., description="Проверено ли")
    addition: AdditionResponseSchema = Field(..., description="Дополнительные данные товара")
    important_numbers: List[int] = Field(..., description="Важные числа")
    
    @field_validator("important_numbers")
    @classmethod
    @allure.step("Проверяем, что список важных чисел не пустой")
    def validate_important_numbers(cls, v: List[int]) -> List[int]:
        if not v:
            logger.error("Список важных чисел не может быть пустым")
            raise ValueError("Список важных чисел не может быть пустым")
        return v
    
    @field_validator("title")
    @classmethod
    @allure.step("Проверяем, что название объекта не пустое и не состоит только из пробелов")
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            logger.error("Название объекта не может быть пустым или состоять только из пробелов")
            raise ValueError("Название объекта не может быть пустым или состоять только из пробелов")
        return v
    
    @field_validator("addition")
    @classmethod
    @allure.step("Проверяем, что дополнительные данные не пустые")
    def validate_addition(cls, v: AdditionResponseSchema) -> AdditionResponseSchema:
        if not v.additional_info.strip():
            logger.error("Дополнительная информация не может быть пустой или состоять только из пробелов")
            raise ValueError("Дополнительная информация не может быть пустой или состоять только из пробелов")
        if len(str(v.additional_number)) == 0:
            logger.error("Дополнительное число не может быть пустым")
            raise ValueError("Дополнительное число не может быть пустым")
        return v

ItemsListResponseSchema.model_rebuild()