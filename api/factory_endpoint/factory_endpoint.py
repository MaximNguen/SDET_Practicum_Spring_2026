from typing import Dict, Literal, Optional, overload
import allure
import logging

from api.base_endpoint import BaseEndpoint
from api.create_item_endpoint import CreateItemEndpoint
from api.delete_item_endpoint import DeleteItemEndpoint
from api.get_item_endpoint import GetItemEndpoint
from api.get_items_endpoint import GetAllItemsEndpoint
from api.update_item_endpoint import UpdateItemEndpoint

logger = logging.getLogger(__name__)

class FactoryEndpoint:
    """Фабрика для создания экземпляров эндпоинтов."""

    EndpointName = Literal["create", "get", "get_all", "patch", "delete"]
    ENDPOINT_CLASSES = {
        "create": CreateItemEndpoint,
        "get": GetItemEndpoint,
        "get_all": GetAllItemsEndpoint,
        "patch": UpdateItemEndpoint,
        "delete": DeleteItemEndpoint,
    }
    
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self._cache: Dict[FactoryEndpoint.EndpointName, BaseEndpoint] = {}
    
    @overload
    def get(self, name: Literal["create"]) -> CreateItemEndpoint:
        ...

    @overload
    def get(self, name: Literal["get"]) -> GetItemEndpoint:
        ...

    @overload
    def get(self, name: Literal["get_all"]) -> GetAllItemsEndpoint:
        ...

    @overload
    def get(self, name: Literal["patch"]) -> UpdateItemEndpoint:
        ...

    @overload
    def get(self, name: Literal["delete"]) -> DeleteItemEndpoint:
        ...
        
    def get(self, name: EndpointName) -> BaseEndpoint:
        endpoint_class = self.ENDPOINT_CLASSES[name]
        if name not in self._cache:
            self._cache[name] = (
                endpoint_class(self.base_url) if self.base_url else endpoint_class()
            )
        return self._cache[name]

    def clear_cache(self) -> None:
        self._cache.clear()