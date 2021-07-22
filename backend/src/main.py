# This is where all starts
from logzero import logger

from backend.src.api.gui_api import GuiApi
from backend.src.config import Config
from backend.src.factory.services_factory import ServicesFactory


def main() -> None:
    config = Config()
    services = ServicesFactory.create_services(config)

    logger.info("API Started Successfully")
    api: GuiApi = services["gui_api"]
    api.start()


if __name__ == "__main__":
    main()
