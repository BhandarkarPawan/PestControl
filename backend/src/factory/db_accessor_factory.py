from typing import Union

from backend.src.config import DBAccessorConfig, DBType
from backend.src.db_accessor.mysql_accessor import MySQLAccessor
from backend.src.db_accessor.sqlite_accessor import SQLiteAccessor


def create_db_accessor(
    db_config: DBAccessorConfig,
) -> Union[MySQLAccessor, SQLiteAccessor]:

    if db_config.db_type == DBType.SQLITE:
        return SQLiteAccessor(db_path=db_config.db_path, echo=db_config.echo,)

    return MySQLAccessor(
        user=db_config.user,
        password=db_config.password,
        address=db_config.password,
        database=db_config.database,
        echo=db_config.echo,
    )
