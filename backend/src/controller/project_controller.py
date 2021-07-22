from typing import List, Optional, Tuple

from logzero import logger

from backend.src.controller.controller import Controller, db_error_check
from backend.src.entities import Project, StatusType


class ProjectController(Controller):
    """Controller class for project entitie"""

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
    def list_projects(self) -> List[Project]:
        projects = self._session.query(Project).all()
        logger.debug(f"Got all projects from the DB: {projects}")
        return projects

    @db_error_check
    def find_project(self, id: int) -> Optional[Project]:
        project = self._session.query(Project).filter(Project.id == id).first()
        logger.debug(f"Got project from the DB: {project}")
        return project

    @db_error_check
    def modify_project(
        self, id: int, title: str, description: str
    ) -> Tuple[StatusType, None]:
        project = self._session.query(Project).filter(Project.id == id).first()
        project.title = title
        project.description = description
        self._session.commit()
        logger.debug(f"Updated project in the DB: {project}")
        return StatusType.SUCCESS, None

    @db_error_check
    def remove_project(self, id: int) -> Tuple[StatusType, None]:
        project = self._session.query(Project).filter(Project.id == id).first()
        self._session.delete(project)
        self._session.commit()
        logger.debug(f"Deleted project from the DB: {project}")
        return StatusType.SUCCESS, None
