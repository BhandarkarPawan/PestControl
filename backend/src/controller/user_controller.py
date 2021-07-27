from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import StatusType, User

# TODO: Add password encryption


class UserController(Controller):
    """Controller class for user entity."""

    # mutations
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
    def modify_user(
        self, name: str = None, email: str = None, password: str = None
    ) -> Tuple[StatusType, Optional[User]]:
        user = self._session.query(User).filter_by(email=email).first()
        if user is None:
            return StatusType.NOT_FOUND, None
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = password
        self._session.commit()
        logger.debug(f"Modified in the DB: {user}")
        return StatusType.SUCCESS, user

    @db_error_check
    def remove_user(self, email: str) -> Tuple[StatusType, Optional[User]]:
        user = self._session.query(User).filter_by(email=email).first()
        if user is None:
            return StatusType.NOT_FOUND, None
        self._session.delete(user)
        self._session.commit()
        logger.debug(f"Removed from the DB: {user}")
        return StatusType.SUCCESS, user

    # queries
    @db_error_check
    def find_user(self, email: str) -> Tuple[StatusType, Optional[User]]:
        user = self._session.query(User).filter_by(email=email).first()
        status_type = StatusType.SUCCESS if user else StatusType.NOT_FOUND
        logger.debug(f"Got user from the DB: {user}")
        return status_type, user

    @db_error_check
    def filter_users(self, name: str) -> Tuple[StatusType, List[User]]:
        users = self._session.query(User)
        if name:
            users = users.filter(User.name.like(f"%{name}%"))
        status_type = StatusType.SUCCESS if len(users) > 0 else StatusType.NOT_FOUND
        logger.debug(f"Got users from the DB: {len(users)}")
        return status_type, users

