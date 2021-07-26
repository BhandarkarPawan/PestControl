from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class API(ABC):
    """
    API interface.
    """

    def _get_graphql_response(
        self, success: bool, error: Optional[str], value: Any = None
    ) -> Dict:
        res = {"success": success, "errors": [error] if error else []}
        if value:
            res["info"] = value
        return res

    @abstractmethod
    def _init_mutations(self) -> None:
        raise NotImplementedError("You need to implement this!")

    @abstractmethod
    def _init_queries(self) -> None:
        raise NotImplementedError("You need to implement this!")
