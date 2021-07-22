import os
from typing import Dict, Tuple, Union

from ariadne import (
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, Response, request
from flask.helpers import send_from_directory
from flask_cors.decorator import cross_origin
from flask_jwt_extended import JWTManager
from logzero import logger

from backend.src.api.jwt_blacklister import JWTBlacklister
from backend.src.api.user_api import UserApi
from backend.src.controller.user_controller import UserController

ApiResponse = Tuple[Union[Dict, Response, str], int]


class GuiApi:
    def __init__(
        self, version: str, port: int, host: str, secret: str, gui_build_path: str,
    ) -> None:
        self._app = Flask(__name__)
        self._cors_allowed_origins = "*"
        self._version = version
        self._port = port
        self._host = host
        self._secret = secret
        self._gui_build_path = gui_build_path
        self._prefix = "/api/"
        self._app.config["JWT_SECRET_KEY"] = self._secret
        self.jwt_blacklister = JWTBlacklister()
        JWTManager(self._app)

    def _init_gui_apis(self) -> None:
        # jwt_blacklister = JWTBlacklister()
        cors_params = {
            "origin": self._cors_allowed_origins,
            "headers": ["Content- Type", "Authorization"],
        }

        current_file_path = os.path.dirname(os.path.realpath(__file__))
        graphql_schema_path = os.path.join(current_file_path, "..", "graphql/")
        type_defs = load_schema_from_path(graphql_schema_path)

        schema = make_executable_schema(
            type_defs,
            self.user_api.query,
            self.user_api.mutation,
            snake_case_fallback_resolvers,
        )

        @self._app.route("/graphql", methods=["GET"])
        @cross_origin(**cors_params)
        def graphql_playground() -> ApiResponse:
            logger.debug("GUI Calls for GET /graphql")
            return PLAYGROUND_HTML, 200

        @self._app.route("/graphql", methods=["POST"])
        # @verify_jwt(jwt_blacklister)
        @cross_origin(**cors_params)
        def graphql_server() -> ApiResponse:
            logger.debug("GUI Calls for POST /graphql")
            data = request.get_json()
            success, result = graphql_sync(schema, data, context_value=request)
            status_code = 200 if success else 400
            return result, status_code

    def _init_gui_paths(self) -> None:

        # make the backend serve the frontend
        logger.warning("Serves the GUI from folder " + self._gui_build_path)

        @self._app.route("/<path:path>")
        def gui_files(path: str) -> Response:
            logger.info("GUI -- %s -> %s", self._gui_build_path, path)
            return send_from_directory(self._gui_build_path, path)

        @self._app.route("/static/<folder>/<filename>")
        def gui_static_files(folder: str, filename: str) -> Response:
            logger.info("GUI -- %s -> %s", self._gui_build_path, filename)
            folderpath = os.path.join(self._gui_build_path, "static", folder)
            return send_from_directory(folderpath, filename)

    def start(self) -> None:
        print(self._app.url_map)
        self._app.run(host=self._host, port=self._port)

    # todo: Add other APIs
    def inject(self, user_controller: UserController, **kwargs) -> None:
        self.user_api = UserApi(user_controller)
        self._init_gui_apis()
        self._init_gui_paths()
