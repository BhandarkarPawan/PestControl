import os
from typing import Optional

from logzero import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.pool import StaticPool

from backend.src.db_accessor.db_accessor import DbAccessor


DEFAULT_DB_FILE_NAME = "agrid_ats.sqlite"


class SQLiteAccessor(DbAccessor):
    def __init__(self, db_path: str, echo: bool) -> None:
        self._engine = self._create_connection_engine(db_path, echo)
        self._connection = self._engine.connect()

    def inject(self, **kwargs) -> None:
        pass

    def get_connection(self) -> Connection:
        return self._connection

    def get_engine(self) -> Engine:
        return self._engine

    def close(self) -> None:
        self._connection.close()

    def _create_connection_engine(self, db_path: Optional[str], echo: bool) -> Engine:
        connection_string = "sqlite://"
        if db_path == ":memory:":
            db_path = None
        if db_path is not None:
            if not db_path.endswith(".sqlite"):
                db_path = os.path.join(db_path, DEFAULT_DB_FILE_NAME)
            db_folder_path = os.path.dirname(db_path)
            if db_folder_path:
                os.makedirs(db_folder_path, exist_ok=True)
            connection_string = connection_string + "/" + db_path
        else:
            logger.info("Use in memory SQLite DB")
        engine = create_engine(
            connection_string,
            connect_args={"check_same_thread": False},
            echo=echo,
            poolclass=StaticPool,
        )
        return engine
