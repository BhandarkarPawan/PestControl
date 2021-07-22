from backend.src.config import Config
from backend.src.factory.db_accessor_factory import create_db_accessor
from backend.src.controller.issue_controller import IssueController
from backend.src.controller.project_controller import ProjectController
from backend.src.controller.user_controller import UserController


def init_db() -> None:
    config = Config()
    db_config = config.db_config
    db_accessor = create_db_accessor(db_config)

    # create controllers
    user_controller = UserController()
    user_controller.inject(db_accessor)

    project_controller = ProjectController()
    project_controller.inject(db_accessor)

    issue_controller = IssueController()
    issue_controller.inject(db_accessor)

    # create 3 dummy users
    _, user1 = user_controller.create_user("user1", "user1@test.com", "password")
    _, user2 = user_controller.create_user("user2", "user2@test.com", "password")
    _, user3 = user_controller.create_user("user3", "user3@test.com", "password")

    # create  dummy project
    _, project = project_controller.create_project("project1", "descr1")

    # create 5 dummy issues
    _, issue1 = issue_controller.create_issue(project.id, "issue1", "desc1", user1.id)
    _, issue2 = issue_controller.create_issue(project.id, "issue2", "desc2", user1.id)
    _, issue3 = issue_controller.create_issue(project.id, "issue3", "desc3", user2.id)
    _, issue4 = issue_controller.create_issue(project.id, "issue4", "desc4", user2.id)
    _, issue5 = issue_controller.create_issue(project.id, "issue5", "desc5", user3.id)


if __name__ == "__main__":
    init_db()
