from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import Issue, StatusType


class IssueController(Controller):
    """Controller class for issue entity."""

    @db_error_check
    def create_issue(
        self,
        project_id: str,
        title: str,
        description: str = None,
        assigned_to: str = None,
        due_date: int = None,
        severity: str = None,
        flag: str = None,
        tags: str = None,
        classification: str = None,
        reproducible: str = None,
    ) -> Tuple[StatusType, Issue]:
        issue = Issue(
            project_id=project_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            severity=severity,
            flag=flag,
            tags=tags,
            classification=classification,
            reproducible=reproducible,
        )

        self._session.add(issue)
        self._session.commit()
        logger.debug(f"Added to the DB: {issue}")
        return StatusType.SUCCESS, issue

    @db_error_check
    def find_issue(self, issue_id: int) -> Tuple[StatusType, Optional[Issue]]:
        issue = self._session.query(Issue).filter(Issue.id == issue_id).first()
        status_type = StatusType.SUCCESS if issue else StatusType.NOT_FOUND
        logger.debug(f"Got issue from the DB: {issue}")
        return status_type, issue

    @db_error_check
    def filter_issues(self, project_id: str) -> Tuple[StatusType, List[Issue]]:
        issues = self._session.query(Issue).filter(Issue.project_id == project_id).all()
        status_type = StatusType.SUCCESS if len(issues) > 0 else StatusType.NOT_FOUND
        logger.debug(f"Got issues from the DB: {len(issues)}")
        return status_type, issues
