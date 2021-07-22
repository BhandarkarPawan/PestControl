from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import StatusType, User


class UserController(Controller):
    """Controller class for user entity."""

    @db_error_check
    def create_user(
        self, name: str, email: str, password: str
    ) -> Tuple[StatusType, User]:
        user = User(name, email, password)
        self._session.add(user)
        self._session.commit()
        logger.debug(f"Added to the DB: {user}")
        return StatusType.SUCCESS, user

    @db_error_check
    def find_user(self, email: str) -> Tuple[StatusType, Optional[User]]:
        user = self._session.query(User).filter_by(email=email).first()
        status_type = StatusType.SUCCESS if user else StatusType.NOT_FOUND
        logger.debug(f"Got project from the DB: {user}")
        return status_type, user

    @db_error_check
    def list_users(self) -> Tuple[StatusType, List[User]]:
        users = self._session.query(User).all()
        status_type = StatusType.SUCCESS if len(users) > 0 else StatusType.NOT_FOUND
        logger.debug(f"Got projects from the DB: {users}")
        return status_type, users

    @db_error_check
    def remove_user(self, email: str) -> Tuple[StatusType, None]:
        _, user = self.find_user(email)
        self._session.session.delete(user)
        logger.debug(f"Deleted user from the DB: {user}")
        return StatusType.SUCCESS, None
