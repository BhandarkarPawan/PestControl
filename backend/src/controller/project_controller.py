from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import Project, StatusType


class ProjectController(Controller):
    """Controller class for project entitie"""

    # mutations
    @db_error_check
    def create_project(
        self, title: str, description: str
    ) -> Tuple[StatusType, Project]:
        project = Project(title=title, description=description)
        self._session.add(project)
        self._session.commit()
        logger.debug(f"Added to the DB: {project}")
        return StatusType.SUCCESS, project

    @db_error_check
    def modify_project(
        self, id: int, title: str = None, description: str = None
    ) -> Tuple[StatusType, Optional[Project]]:
        project = self._session.query(Project).filter(Project.id == id).first()
        if project is None:
            return StatusType.NOT_FOUND, None
        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        self._session.commit()
        logger.debug(f"Modified in the DB: {project}")
        return StatusType.SUCCESS, project

    @db_error_check
    def remove_project(self, id: int) -> Tuple[StatusType, Optional[Project]]:
        project = self._session.query(Project).filter(Project.id == id).first()
        if project is None:
            return StatusType.NOT_FOUND, None
        self._session.delete(project)
        self._session.commit()
        logger.debug(f"Removed from the DB: {project}")
        return StatusType.SUCCESS, project

    # queries
    @db_error_check
    def find_project(self, id: int) -> Tuple[StatusType, Optional[Project]]:
        project = self._session.query(Project).filter(Project.id == id).first()
        logger.debug(f"Got project from the DB: {project}")
        return StatusType.SUCCESS, project

    @db_error_check
    def filter_projects(self, name: str = None) -> Tuple[StatusType, List[Project]]:
        projects = self._session.query(Project)
        if name:
            projects = projects.filter(Project.title.like(f"%{name}%"))
        logger.debug(f"Got all projects from the DB: {projects}")
        return projects

