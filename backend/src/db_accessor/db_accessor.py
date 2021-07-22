from abc import ABC, abstractmethod

from sqlalchemy.engine import Connection, Engine


class DbAccessor(ABC):
    @abstractmethod
    def get_connection(self) -> Connection:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def get_engine(self) -> Engine:
        raise NotImplementedError("You should implement this!")

    @abstractmethod
    def inject(self, **kwargs) -> None:
        raise NotImplementedError("You should implement this!")
