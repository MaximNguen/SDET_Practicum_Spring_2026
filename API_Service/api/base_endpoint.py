from abc import abstractmethod, ABC
from typing import Any, Dict, Optional
import allure
from pydantic import ValidationError
import logging
import requests

from config import BASE_URL, HEADERS, CREATE_URL, DELETE_URL, GET_ALL_URL, GET_BY_ID_URL, PATCH_URL, TIMEOUT_SECONDS
from utils.api.api_validators import extract_item_id_from_create_response

logger = logging.getLogger(__name__)

class BaseEndpoint(ABC):
    """
    Базовый класс для всех API-эндпоинтов.
    Содержит общие методы для отправки HTTP-запросов и обработки ответов.
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.create_url = f"{self.base_url}{CREATE_URL}"
        self.delete_url = f"{self.base_url}{DELETE_URL}"
        self.get_all_url = f"{self.base_url}{GET_ALL_URL}"
        self.get_by_id_url = f"{self.base_url}{GET_BY_ID_URL}"
        self.patch_url = f"{self.base_url}{PATCH_URL}"
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.response: Optional[requests.Response] = None
        self.response_json: Optional[Dict[str, Any]] = None

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass
    
    @allure.step("Проверюяем, что код статуса - {expected_code}")
    def check_status_code(self, expected_code: int) -> None:
        logger.info(f"Проверяем, что код статуса - {expected_code}")
        assert self.response is not None, "Код статуса не пришел"
        actual_code = self.response.status_code
        assert (
            actual_code == expected_code
        ), f"Ожидали {expected_code}, получили {actual_code}. Ответ: {self.response.text}"
            
    @allure.step("Достаем Id у объекта из ответа")
    def extract_item_id(self) -> Optional[str]:
        logger.info("Достаем Id у объекта из ответа")
        if not self.response_json:
            return None

        try:
            return extract_item_id_from_create_response(self.response_json)
        except (ValidationError, ValueError, TypeError):
            return None