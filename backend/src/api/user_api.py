from typing import Optional, Dict

from ariadne import ObjectType
from logzero import logger

from backend.src.controller.user_controller import UserController
from backend.src.entities import User
from backend.src.api.api import API


class UserApi(API):
    def __init__(self, user_controller: UserController) -> None:
        self.controller = user_controller
        self.query = ObjectType("Query")
        self.mutation = ObjectType("Mutation")

        self._init_queries()
        self._init_mutations()

    def _init_mutations(self) -> None:
        self.mutation.set_field("addUser", self.add_user)

    def _init_queries(self) -> None:
        self.query.set_field("getUser", self.get_user)
        self.query.set_field("getUsers", self.get_users)

    # mutation methods
    def add_user(self) -> Optional[User]:
        logger.info("GUI calls for addUser mutation")
        raise NotImplementedError("You need to implement this!")

    # query methods
    def get_user(self, *args, **kwargs) -> Dict:
        logger.info("GUI calls for getUser query")
        success, user = self.controller.find_user(**kwargs)
        return {"success": True, "errors": [], "info": user}

    def get_users(self, *args, **kwargs) -> Dict:
        logger.info("GUI calls for getUsers query")
        success, users = self.controller.list_users(**kwargs)
        return {"success": True, "errors": [], "info": users}
