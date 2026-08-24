import logging
import re

logger = logging.getLogger(__name__)


def parse_money_value(text: str) -> float:
    """Преобразовать денежный текст в float."""
    cleaned = text.strip().replace("$", "").replace(" ", "").replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    if not match:
        logger.error(f"Не удалось распарсить денежное значение: '{text}'")
        raise ValueError(f"Не удалось распарсить денежное значение: {text}")
    return float(match.group(0))
