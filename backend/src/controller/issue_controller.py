from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import Issue, StatusType


class IssueController(Controller):
    """Controller class for issue entity."""

    # mutations
    @db_error_check
    def create_issue(
        self,
        project_id: str,
        title: str,
        reported_by: str,
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
            reported_by=reported_by,
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
    def modify_issue(
        self,
        id: int,
        title: str = None,
        description: str = None,
        assigned_to: str = None,
        due_date: int = None,
        severity: str = None,
        flag: str = None,
        tags: str = None,
        classification: str = None,
        reproducible: str = None,
    ) -> Tuple[StatusType, Optional[Issue]]:
        issue = self._session.query(Issue).filter_by(id=id).first()
        if issue is None:
            return StatusType.NOT_FOUND, None
        if title is not None:
            issue.title = title
        if description is not None:
            issue.description = description
        if assigned_to is not None:
            issue.assigned_to = assigned_to
        if due_date is not None:
            issue.due_date = due_date
        if severity is not None:
            issue.severity = severity
        if flag is not None:
            issue.flag = flag
        if tags is not None:
            issue.tags = tags
        if classification is not None:
            issue.classification = classification
        if reproducible is not None:
            issue.reproducible = reproducible
        self._session.commit()
        logger.debug(f"Modified in the DB: {issue}")
        return StatusType.SUCCESS, issue

    @db_error_check
    def remove_issue(self, id: int) -> Tuple[StatusType, Optional[Issue]]:
        issue = self._session.query(Issue).filter_by(id=id).first()
        if issue is None:
            return StatusType.NOT_FOUND, None
        self._session.delete(issue)
        self._session.commit()
        logger.debug(f"Removed from the DB: {issue}")
        return StatusType.SUCCESS, issue

    # queries
    @db_error_check
    def find_issue(self, issue_id: int) -> Tuple[StatusType, Optional[Issue]]:
        issue = self._session.query(Issue).filter(Issue.id == issue_id).first()
        status_type = StatusType.SUCCESS if issue else StatusType.NOT_FOUND
        logger.debug(f"Got issue from the DB: {issue}")
        return status_type, issue

    @db_error_check
    def filter_issues(
        self,
        project_id: str = None,
        title: str = None,
        assigned_to: str = None,
        reported_date: int = None,
        due_date: int = None,
        severity: str = None,
        flag: str = None,
        classification: str = None,
        reproducible: str = None,
    ) -> Tuple[StatusType, List[Issue]]:
        issues = self._session.query(Issue)
        if project_id:
            issues = issues.filter(Issue.project_id == project_id)
        if title:
            issues = issues.filter(Issue.title.like(f"%{title}%"))
        if assigned_to:
            issues = issues.filter(Issue.assigned_to == assigned_to)
        if reported_date:
            issues = issues.filter(Issue.reported_date == reported_date)
        if due_date:
            issues = issues.filter(Issue.due_date == due_date)
        if severity:
            issues = issues.filter(Issue.severity == severity)
        if flag:
            issues = issues.filter(Issue.flag == flag)
        if classification:
            issues = issues.filter(Issue.classification == classification)
        if reproducible:
            issues = issues.filter(Issue.reproducible == reproducible)

        issues = list(issues)
        status_type = StatusType.SUCCESS if len(issues) > 0 else StatusType.NOT_FOUND
        logger.debug(f"Got issues from the DB: {len(issues)}")
        return status_type, issues
