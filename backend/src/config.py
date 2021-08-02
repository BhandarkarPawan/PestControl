from collections import defaultdict
from configparser import ConfigParser
from enum import Enum
import os
from typing import cast
from typing import Any, Dict

from logzero import logger

API_ROOT_FOLDER = os.path.join(os.path.dirname(__file__), "..")
CONFIG_INI_PATH = os.path.join(API_ROOT_FOLDER, "config.ini")


# -------------- Helper Functions --------------#


def _BOOL(x: str) -> bool:
    return x in ["True", "TRUE", "true", "1"]


def ensure_config(config, key: str) -> Dict:
    config = config[key] if key in config else defaultdict(lambda: None)
    return cast(Dict, config)


def ensure_value(config_dict: Dict, key: str, value: Any, cb) -> Any:
    if key not in config_dict:
        logger.warning(
            f"Config {key} missing in config file. Using the default value. "
            "This may lead to unexpected behavior."
        )
        return value
    return cb(config_dict[key])


def get_absolute_path(file_path: str) -> str:
    path = cast(str, file_path)
    return os.path.join(API_ROOT_FOLDER, path)


# -------------- Enum Types --------------#


class DBType(Enum):
    SQLITE = "SQLITE"
    MYSQL = "MYSQL"


class ImageStoreType(Enum):
    S3 = "S3"
    LOCAL = "LOCAL"


# -------------- Config Types --------------#


class ImageAccessorConfig:
    store_type: ImageStoreType
    folder_path: str
    s3_public_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_region: str

    def __init__(
        self,
        store_type: ImageStoreType,
        folder_path: str,
        s3_public_key: str,
        s3_secret_key: str,
        s3_bucket: str,
        s3_region: str,
    ) -> None:
        self.store_type = store_type
        self.folder_path = folder_path
        self.s3_public_key = s3_public_key
        self.s3_secret_key = s3_secret_key
        self.s3_bucket = s3_bucket
        self.s3_region = s3_region


class APIConfig:
    version: str
    port: int
    host: str
    secret: str
    gui_build_path: str

    def __init__(
        self, version: str, port: int, host: str, secret: str, gui_build_path: str
    ) -> None:
        self.version = version
        self.port = port
        self.host = host
        self.secret = secret
        self.gui_build_path = gui_build_path


class LoggerConfig:
    file_path: str
    log_level: str

    def __init__(self, file_path: str, log_level: str) -> None:
        self.log_level = log_level
        self.file_path = file_path


class DBAccessorConfig:
    echo: bool
    db_type: DBType
    db_path: str
    user: str
    password: str
    address: str
    database: str

    def __init__(
        self,
        echo: bool,
        db_type: DBType,
        db_path: str,
        user: str,
        password: str,
        address: str,
        database: str,
    ) -> None:
        self.echo = echo
        self.db_type = db_type
        self.db_path = db_path
        self.user = user
        self.password = password
        self.address = address
        self.database = database


class Config:
    api_config: APIConfig
    logger_config: LoggerConfig
    db_config: DBAccessorConfig
    image_config: ImageAccessorConfig

    def __init__(self) -> None:
        config = ConfigParser(inline_comment_prefixes=";")
        config.read(CONFIG_INI_PATH)

        api_config = ensure_config(config, "api")
        self.api_config = APIConfig(
            version=ensure_value(api_config, "version", "v1", str),
            port=ensure_value(api_config, "port", 5000, int),
            host=ensure_value(api_config, "host", "0.0.0.0", str),
            secret=ensure_value(api_config, "secret", "jwtsecret", str),
            gui_build_path=ensure_value(
                api_config, "gui_build_path", "../gui/src", get_absolute_path
            ),
        )

        logger_config = ensure_config(config, "logger")
        self.logger_config = LoggerConfig(
            log_level=ensure_value(logger_config, "log_level", "debug", str),
            file_path=ensure_value(
                logger_config, "file_path", "resources/logs.log", get_absolute_path
            ),
        )

        db_config = ensure_config(config, "database")
        self.db_config = DBAccessorConfig(
            echo=ensure_value(db_config, "echo", False, _BOOL),
            db_type=ensure_value(db_config, "type", DBType.SQLITE, DBType),
            db_path=ensure_value(db_config, "db_path", ":memory:", get_absolute_path),
            user=ensure_value(db_config, "user", "", str),
            password=ensure_value(db_config, "password", "", str),
            address=ensure_value(db_config, "address", "", str),
            database=ensure_value(db_config, "database", "", str),
        )

        image_config = ensure_config(config, "image")
        self.image_config = ImageAccessorConfig(
            store_type=ensure_value(
                image_config, "type", ImageStoreType.LOCAL, ImageStoreType
            ),
            folder_path=ensure_value(
                image_config, "folder_path", "resources/images", get_absolute_path
            ),
            s3_public_key=ensure_value(image_config, "s3_public_key", "", str),
            s3_secret_key=ensure_value(image_config, "s3_secret_key", "", str),
            s3_bucket=ensure_value(image_config, "s3_bucket", "", str),
            s3_region=ensure_value(image_config, "s3_region", "", str),
        )

