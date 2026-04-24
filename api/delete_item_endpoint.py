import allure
import logging

from api.base_endpoint import BaseEndpoint

logger = logging.getLogger(__name__)

class DeleteItemEndpoint(BaseEndpoint):
    """Эндпоинт для удаления товара по ID."""

    @allure.step("Удаляем товар с ID: {item_id}")
    def action(self, item_id: int):
        logger.info(f"Удаляем товар с ID: {item_id}")
        self.response = self.session.delete(f"{self.delete_url}{item_id}")
        return self.response.status_code
    
    @allure.step("Удаляем товар с ID: {item_id}, ожидая ошибку с кодом {expected_code}")
    def action_expect_error(self, item_id: int, expected_code: int):
        """Удаляем товар с ID: {item_id}, ожидая ошибку с кодом {expected_code}"""
        logger.info(f"Удаляем товар с ID: {item_id}, ожидая ошибку с кодом {expected_code}")
        self.response = self.session.delete(f"{self.delete_url}{item_id}")
        return self.check_status_code(expected_code) 