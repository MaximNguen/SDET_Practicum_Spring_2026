import json
import logging
import allure
from pathlib import Path
from typing import Any, Dict, Optional

from utils.api.api_validators import validate_create_item_response
from utils.api.generators import Generator

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "data" / "api_data" / "item_payloads.json"

@allure.step("Загружаем полезную нагрузку из JSON-файла по имени")
def load_payload() -> Dict[str, Any]:
    """Загружает полезную нагрузку из JSON-файла по имени."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            payloads = json.load(f)
        return payloads
    except Exception as e:
        logger.error(f"Ошибка при загрузке полезной нагрузки: {e}")
        raise
    
@allure.step("Строим полезную нагрузку на основе шаблона из JSON-файла и дополнительных параметров")
def build_payload() -> Dict[str, Any]:
    """Строит полезную нагрузку на основе шаблона из JSON-файла и дополнительных параметров."""
    payload = load_payload()
    payload["title"] = Generator.generate_random_string(10)
    payload["important_numbers"] = [Generator.generate_random_number(1, 100) for _ in range(3)]
    payload["verified"] = True
    payload["addition"] = {
        "additional_info": Generator.generate_random_string(20),
        "additional_number": Generator.generate_random_number(1, 100)
    }
    try:
        validate_create_item_response(payload)
        return payload
    except Exception as e:
        logger.error(f"Ошибка при валидации загрузки: {e}")
        raise ValueError(f"Ошибка при валидации загрузки: {e}")