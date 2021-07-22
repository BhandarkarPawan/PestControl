from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

from backend.src.db_accessor.db_accessor import DbAccessor


class MySQLAccessor(DbAccessor):
    def __init__(
        self, user: str, password: str, address: str, database: str, echo: bool
    ) -> None:
        engine = self._create_connection_engine(user, password, address, database, echo)
        self._connection = engine.connect()
        self._engine = engine

    def inject(self, **kwargs) -> None:
        pass

    def get_connection(self) -> Connection:
        return self._connection

    def get_engine(self) -> Engine:
        return self._engine

    def _create_connection_engine(
        self, user: str, password: str, address: str, database: str, echo: bool
    ) -> Engine:
        connection_string = "mysql://{0}:{1}@{2}/{3}".format(
            user, password, address, database
        )
        engine = create_engine(connection_string, echo=echo)
        return engine
