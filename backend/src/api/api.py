from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict

from flask import Request
from flask_jwt_extended import decode_token

from backend.src.entities import StatusType


class API(ABC):
    """
    API interface.
    """

    def get_logged_in_user(self, request: Request):
        user_dict = None
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            scheme, token = auth.split()
            if scheme.lower() == "bearer":
                user_dict = decode_token(token)["sub"]
        return user_dict

    # Helper methods
    def _get_graphql_response(self, status: StatusType, value: Any = None) -> Dict:
        success = status == StatusType.SUCCESS
        errors = [] if success else [status.value]
        res = {"success": success, "errors": errors, "info": value}
        return res

    def _format_date(self, date: int) -> str:
        return datetime.fromtimestamp(date).strftime("%d-%m-%Y")

    @abstractmethod
    def _init_mutations(self) -> None:
        raise NotImplementedError("You need to implement this!")

    @abstractmethod
    def _init_queries(self) -> None:
        raise NotImplementedError("You need to implement this!")

    @abstractmethod
    def _init_objects(self) -> None:
        raise NotImplementedError("You need to implement this!")
