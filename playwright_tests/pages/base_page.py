import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    """Базовая страница для всех страниц приложения (Playwright).

    В отличие от Selenium-версии здесь нет кастомных ожиданий
    (WaitHelpers) и нормализации локаторов — Playwright автоматически
    ждёт появления и кликабельности элементов.
    """

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        logger.info(f"Открываем страницу по URL: {url}")
        self.page.goto(url)

    def get_current_url(self) -> str:
        return self.page.url

    def go_back(self) -> None:
        self.page.go_back()
