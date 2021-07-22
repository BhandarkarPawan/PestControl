""" Imports and initializes all the Services"""

from typing import Dict

from backend.src.api.gui_api import GuiApi
from backend.src.config import Config
from backend.src.controller.issue_controller import IssueController
from backend.src.controller.project_controller import ProjectController
from backend.src.controller.user_controller import UserController
from backend.src.factory.db_accessor_factory import create_db_accessor
from backend.src.logger import setup_global_logger


class ServicesFactory:
    """
    A class used to initialize the services

    Methods
    -------
    create_services(config)
        Uses tthe config object to configure each service
    """

    @staticmethod
    def create_services(config: Config) -> Dict:
        """Creates a dictionary of key -> Service mapping"""

        api_config = config.api_config
        db_config = config.db_config
        logger_config = config.logger_config

        setup_global_logger(file_path=logger_config.file_path)

        services = {
            "gui_api": GuiApi(
                version=api_config.version,
                host=api_config.host,
                port=api_config.port,
                secret=api_config.secret,
                gui_build_path=api_config.gui_build_path,
            ),
            "user_controller": UserController(),
            "project_controller": ProjectController(),
            "issue_controller": IssueController(),
            # ----Factory Methods ----#
            "db_accessor": create_db_accessor(db_config),
        }

        for _, service in services.items():
            service.inject(**services)

        return services
