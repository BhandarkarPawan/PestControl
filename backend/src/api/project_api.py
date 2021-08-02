from typing import Dict

from ariadne import QueryType, MutationType, ObjectType
from logzero import logger

from backend.src.api.api import API
from backend.src.controller.project_controller import ProjectController


class ProjectApi(API):
    def __init__(self, project_controller: ProjectController) -> None:
        self.controller = project_controller
        self.query = QueryType()
        self.mutation = MutationType()
        self.object = ObjectType("Project")

        self._init_queries()
        self._init_mutations()
        self._init_objects()

    def _init_mutations(self) -> None:
        self.mutation.set_field("addProject", self.add_project)
        self.mutation.set_field("updateProject", self.update_project)
        self.mutation.set_field("deleteProject", self.delete_project)

    def _init_queries(self) -> None:
        self.query.set_field("getProject", self.get_project)
        self.query.set_field("searchProjects", self.search_projects)

    def _init_objects(self) -> None:
        pass

    # mutation methods
    def add_project(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for addProject mutation")
        status, project = self.controller.create_project(**kwargs)
        return self._get_graphql_response(status, project)

    def update_project(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for updateProject mutation")
        status, project = self.controller.modify_project(**kwargs)
        return self._get_graphql_response(status, project)

    def delete_project(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for deleteProject mutation")
        status, project = self.controller.remove_project(**kwargs)
        return self._get_graphql_response(status, project)

    # query methods
    def get_project(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for getProject query")
        status, project = self.controller.find_project(**kwargs)
        return self._get_graphql_response(status, project)

    def search_projects(self, *_, **kwargs) -> Dict:
        logger.info("GUI calls for getProjects query")
        status, projects = self.controller.filter_projects(**kwargs)
        return self._get_graphql_response(status, projects)

