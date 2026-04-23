import random
import logging

logger = logging.getLogger(__name__)

class Generator:
    """Класс для генерации случайных данных для тестов."""
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Генерирует случайную строку заданной длины."""
        logger.info(f"Генерируем случайную строку длиной {length} - работа Генератора")
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return "".join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def generate_random_number(min_value: int = 1, max_value: int = 100) -> int:
        """Генерирует случайное число в заданном диапазоне."""
        logger.info(f"Генерируем случайное число в диапазоне [{min_value}, {max_value}] - работа Генератора")
        return random.randint(min_value, max_value)