from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class DbAccessor(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def get_engine(self) -> Engine:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def inject(self, **kwargs) -> None:
        raise NotImplementedError("You should implement this!")
