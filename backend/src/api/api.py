from abc import ABC, abstractmethod
from typing import Any, Dict

from backend.src.entities import StatusType


class API(ABC):
    """
    API interface.
    """

    def _get_graphql_response(self, status: StatusType, value: Any = None) -> Dict:
        success = status == StatusType.SUCCESS
        errors = [] if success else [status.value]
        res = {"success": success, "errors": errors}
        if value:
            res["info"] = value
        return res

    @abstractmethod
    def _init_mutations(self) -> None:
        raise NotImplementedError("You need to implement this!")

    @abstractmethod
    def _init_queries(self) -> None:
        raise NotImplementedError("You need to implement this!")
