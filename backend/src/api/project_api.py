from typing import Optional

from ariadne import ObjectType
from logzero import logger

from backend.src.controller.project_controller import ProjectController
from backend.src.entities import Project


class ProjectApi:
    def __init__(self, project_controller: ProjectController) -> None:
        self.controller = project_controller
        self.query = ObjectType("Query")
        self.mutation = ObjectType("Mutation")

        self._init_queries()
        self._init_mutations()

    def _init_mutations(self) -> None:
        self.mutation.set_field("addProject", self.add_project)

    def _init_queries(self) -> None:
        self.query.set_field("getProject", self.get_project)

    # mutation methods
    def add_project(self) -> Optional[Project]:
        logger.info("GUI calls for addProject mutation")
        raise NotImplementedError("You need to implement this!")

    # query methods
    def get_project(self) -> Optional[Project]:
        logger.info("GUI calls for getProject query")
        raise NotImplementedError("You need to implement this!")
