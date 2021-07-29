from typing import Dict

from ariadne import ObjectType
from logzero import logger

from backend.src.controller.user_controller import UserController
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
        self.mutation.set_field("updateUser", self.update_user)
        self.mutation.set_field("deleteUser", self.delete_user)

    def _init_queries(self) -> None:
        self.query.set_field("getUser", self.get_user)
        self.query.set_field("searchUsers", self.search_users)

    # mutation methods
    def add_user(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for addUser mutation")
        status, user = self.controller.create_user(**kwargs)
        return self._get_graphql_response(status, user)

    def update_user(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for updateUser mutation")
        status, user = self.controller.modify_user(**kwargs)
        return self._get_graphql_response(status, user)

    def delete_user(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for removeUser mutation")
        status, user = self.controller.remove_user(**kwargs)
        return self._get_graphql_response(status, user)

    # query methods
    def get_user(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for getUser query")
        status, user = self.controller.find_user(**kwargs)
        return self._get_graphql_response(status, user)

    def search_users(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for getUsers query")
        status, users = self.controller.filter_users(**kwargs)
        return self._get_graphql_response(status, users)
