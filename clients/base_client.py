from typing import Any, Dict, Optional
import requests
import logging
import allure

from config import BASE_URL, TIMEOUT_SECONDS, HEADERS

logger = logging.getLogger(__name__)

class BaseClient:
    """
    Базовый клиент для взаимодействия с API.
    Содержит общие методы для отправки HTTP-запросов и обработки ответов.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: int = TIMEOUT_SECONDS
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def send_request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Отправка запроса и принятие ответа"""
        url = f"{self.base_url}{path}"
        with allure.step(f"Отправляем {method} запрос на URL: {url}{path} с данными: {json}"):
            logger.info(f"Отправляем {method} запрос на URL: {url}{path} с данными: {json}")
            try:
                return self.session.request(
                    method=method,
                    url=url,
                    json=json,
                    timeout=self.timeout_seconds,
                )
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка при отправке запроса: {e}")
                raise