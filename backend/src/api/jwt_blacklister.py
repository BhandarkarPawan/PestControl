import time
from typing import Any, Dict, List

from flask import Response, jsonify
from flask_jwt_extended import get_jwt, jwt_required


# helper functions
def get_basic_response(success_flag: bool, info: Any) -> Response:
    return jsonify({"success": success_flag, "info": info})


class Token:
    jti: str
    exp: int

    def __init__(self, jwt: Dict) -> None:
        self.jti = jwt["jti"]
        self.exp = jwt["exp"]

    def is_valid(self) -> bool:
        return time.time() < self.exp


class JWTBlacklister:
    _max_blacklist_size: float = 1e4
    _blacklist: List[Token] = []

    def _refresh_blacklist(self) -> None:
        self._blacklist = [token for token in self._blacklist if token.is_valid()]

    def is_valid(self, token: Token) -> bool:
        self._refresh_blacklist()
        for t in self._blacklist:
            if token.jti == t.jti:
                return False
        return True

    def invalidate(self, jwt: Dict) -> None:
        self._refresh_blacklist()
        token = Token(jwt)
        self._blacklist.append(token)
        if len(self._blacklist) == self._max_blacklist_size:
            self._blacklist = self._blacklist[1:]  # discard oldest


def verify_jwt(jwt_blacklister: JWTBlacklister):
    def decorator(function):
        @jwt_required()
        def wrapper(*args, **kwargs):
            jwt: Dict = get_jwt()
            token = Token(jwt)
            if jwt_blacklister.is_valid(token):
                return function(*args, **kwargs)
            return get_basic_response(False, "You have been logged out."), 401

        return wrapper

    return decorator
