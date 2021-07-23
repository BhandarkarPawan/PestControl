from typing import Optional

from ariadne import ObjectType
from logzero import logger

from backend.src.controller.issue_controller import IssueController
from backend.src.entities import Issue


class IssueApi:
    def __init__(self, issue_controller: IssueController) -> None:
        self.controller = issue_controller
        self.query = ObjectType("Query")
        self.mutation = ObjectType("Mutation")

        self._init_queries()
        self._init_mutations()

    def _init_mutations(self) -> None:
        self.mutation.set_field("addIssue", self.add_issue)

    def _init_queries(self) -> None:
        self.query.set_field("getIssue", self.get_issue)

    # mutation methods
    def add_issue(self) -> Optional[Issue]:
        logger.info("GUI calls for addIssue mutation")
        raise NotImplementedError("You need to implement this!")

    # query methods
    def get_issue(self) -> Optional[Issue]:
        logger.info("GUI calls for getIssue query")
        raise NotImplementedError("You need to implement this!")
