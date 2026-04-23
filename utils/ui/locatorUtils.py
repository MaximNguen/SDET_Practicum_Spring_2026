class LocatorUtils:
    """Класс для работы с локаторами"""

    @staticmethod
    def normalize_locator(locator: tuple) -> tuple:
        """Нормализовать локатор до пары (by, value)."""
        if len(locator) == 1 and isinstance(locator[0], tuple):
            locator = locator[0]
        return locator
