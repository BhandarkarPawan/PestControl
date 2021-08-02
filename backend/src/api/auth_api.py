from typing import Dict

from flask import Flask
from flask_cors.decorator import cross_origin
from flask_jwt_extended import create_access_token, get_jwt
from logzero import logger

from backend.src.api.api import API
from backend.src.api.jwt_blacklister import JWTBlacklister, verify_jwt
from backend.src.controller.user_controller import UserController
from backend.src.entities import StatusType


class AuthApi(API):
    def __init__(
        self,
        app: Flask,
        jwt_blacklister: JWTBlacklister,
        cors_params: Dict,
        user_controller: UserController,
    ) -> None:
        self.app = app
        self.controller = user_controller
        self.blacklister = jwt_blacklister
        self.cors_params = cors_params

        self._init_api()

    def _init_mutations(self) -> None:
        pass

    def _init_queries(self) -> None:
        pass

    def _init_objects(self) -> None:
        pass

    # authentication methods
    def _init_api(self) -> None:
        @self.app.route("/auth", methods=["POST"])
        @cross_origin(**self.cors_params)
        def signup(*_, **kwargs) -> Dict:
            logger.info("GUI calls for singup")
            status, _ = self.controller.create_user(**kwargs)
            return self._get_graphql_response(status)

        @self.app.route("/auth", methods=["PUT"])
        @cross_origin(**self.cors_params)
        def signin(*_, **kwargs) -> Dict:
            logger.info("GUI calls for signin")
            status, user = self.controller.authenticate_user(**kwargs)
            token = create_access_token(identity=user.email) if user else ""
            return self._get_graphql_response(status, token)

        @self.app.route("/auth", methods=["DELETE"])
        @cross_origin(**self.cors_params)
        @verify_jwt(self.blacklister)
        def signout(*_, **kwargs) -> Dict:
            logger.info("GUI calls for signout")
            self.blacklister.invalidate(get_jwt())
            status = StatusType.SUCCESS
            return self._get_graphql_response(status)
