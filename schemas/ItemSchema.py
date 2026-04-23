import re
from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class ItemRequestSchema(BaseModel):
    """Схема для создания и обновления товара."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    addition: AdditionRequestSchema = Field(..., description="Дополнительные данные товара")
    important_numbers: List[int] = Field(..., description="Важные числа")
    title: str = Field(..., description="Название объекта", min_length=1)
    verified: bool = Field(..., description="Проверено ли")
    
    @field_validator("important_numbers")
    @classmethod
    def validate_important_numbers(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("Список важных чисел не может быть пустым")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Название объекта не может быть пустым или состоять только из пробелов")
        return v
    
    @field_validator("addition")
    @classmethod
    def validate_addition(cls, v: AdditionRequestSchema) -> AdditionRequestSchema:
        if not v.additional_info.strip():
            raise ValueError("Дополнительная информация не может быть пустой или состоять только из пробелов")
        if len(str(v.additional_number)) == 0:
            raise ValueError("Дополнительное число не может быть пустым")
        return v
    

class AdditionRequestSchema(BaseModel):
    """Схема для поля addition."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    additional_info: str = Field(..., description="Дополнительная информация", min_length=1)
    additional_number: int = Field(..., description="Дополнительное число", ge=0)
    
class ItemResponseSchema(BaseModel):
    """Схема для ответа при получении товара."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    id: int = Field(..., description="Уникальный идентификатор товара", ge=0)
    title: str = Field(..., description="Название объекта", min_length=1)
    verified: bool = Field(..., description="Проверено ли")
    addition: AdditionResponseSchema = Field(..., description="Дополнительные данные товара")
    important_numbers: List[int] = Field(..., description="Важные числа")
    
    @field_validator("important_numbers")
    @classmethod
    def validate_important_numbers(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("Список важных чисел не может быть пустым")
        return v
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Название объекта не может быть пустым или состоять только из пробелов")
        return v
    
    @field_validator("addition")
    @classmethod
    def validate_addition(cls, v: AdditionRequestSchema) -> AdditionRequestSchema:
        if not v.additional_info.strip():
            raise ValueError("Дополнительная информация не может быть пустой или состоять только из пробелов")
        if len(str(v.additional_number)) == 0:
            raise ValueError("Дополнительное число не может быть пустым")
        return v

class AdditionResponseSchema(BaseModel):
    """Схема для поля addition в ответе."""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    id: int = Field(..., description="Уникальный идентификатор дополнительных данных", ge=0)
    additional_info: str = Field(..., description="Дополнительная информация", min_length=1)
    additional_number: int = Field(..., description="Дополнительное число", ge=0)
    
class ItemsListResponseSchema(BaseModel):
    """Схема для ответа со списком объектов."""
    entity: List[ItemResponseSchema] = Field(..., description="Список объектов")