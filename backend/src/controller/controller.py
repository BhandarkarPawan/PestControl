from abc import ABC
from functools import wraps
import traceback
from typing import List, Tuple

from logzero import logger
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import IntegrityError, ProgrammingError, SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from backend.src.db_accessor.db_accessor import DbAccessor
from backend.src.entities import Base, StatusType


def db_error_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            logger.debug("The DB Query result passed checks.")
            return result
        except IntegrityError as e:
            logger.error(e)
            traceback.print_exc()
            return StatusType.CONSTRAINT_ERROR, None
        except ProgrammingError as e:
            logger.error(e)
            traceback.print_exc()
            return StatusType.INPUT_ERROR, None
        except SQLAlchemyError as e:
            logger.error(e)
            traceback.print_exc()
            return StatusType.DATABASE_ERROR, None
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            return StatusType.SERVER_ERROR, None

    return decorated


class Controller(ABC):
    def inject(self, db_accessor: DbAccessor, **kwargs) -> None:
        self._engine: Engine = db_accessor.get_engine()
        self._connection: Connection = db_accessor.get_connection()
        self._session: Session = scoped_session(
            sessionmaker(autocommit=False, autoflush=True, bind=self._engine)
        )

        # Create tables if they do not exist
        Base.metadata.create_all(self._engine)

    def list_distinct(self, db_list: List[Tuple]) -> List:
        return sorted([x[0] for x in db_list if x[0] is not None])
