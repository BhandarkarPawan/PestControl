from typing import Dict

from ariadne import MutationType, ObjectType, QueryType
from logzero import logger

from backend.src.api.api import API
from backend.src.entities import Issue
from backend.src.controller.issue_controller import IssueController


class IssueApi(API):
    def __init__(self, issue_controller: IssueController) -> None:
        self.controller = issue_controller
        self.query = QueryType()
        self.mutation = MutationType()
        self.object = ObjectType("Issue")

        self._init_queries()
        self._init_mutations()
        self._init_objects()

    def _init_mutations(self) -> None:
        self.mutation.set_field("addIssue", self.add_issue)
        self.mutation.set_field("updateIssue", self.update_issue)
        self.mutation.set_field("deleteIssue", self.delete_issue)

    def _init_queries(self) -> None:
        self.query.set_field("getIssue", self.get_issue)
        self.query.set_field("searchIssues", self.search_issues)

    def _init_objects(self) -> None:
        self.object.set_field("reportedDate", self.format_reported_date)
        self.object.set_field("dueDate", self.format_due_date)

    # mutation methods
    def add_issue(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for addIssue mutation")
        status, issue = self.controller.create_issue(**kwargs)
        return self._get_graphql_response(status, issue)

    def update_issue(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for updateIssue mutation")
        status, issue = self.controller.modify_issue(**kwargs)
        return self._get_graphql_response(status, issue)

    def delete_issue(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for removeUser mutation")
        status, user = self.controller.remove_issue(**kwargs)
        return self._get_graphql_response(status, user)

    # query methods
    def get_issue(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for getIssue query")
        status, issue = self.controller.find_issue(**kwargs)
        return self._get_graphql_response(status, issue)

    def search_issues(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for searchIssues query")
        status, issue = self.controller.filter_issues(**kwargs)
        return self._get_graphql_response(status, issue)

    # object methods
    def format_reported_date(self, obj: Issue, *_) -> str:
        date = obj.reported_date
        return self._format_date(date)

    def format_due_date(self, obj: Issue, *_) -> str:
        date = obj.due_date
        return self._format_date(date)
