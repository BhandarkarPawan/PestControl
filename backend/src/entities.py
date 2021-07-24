from enum import Enum
from time import time

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class StatusType(Enum):
    CONSTRAINT_ERROR = "CONSTRAINT_ERROR"
    SERVER_ERROR = "SERVER_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    INPUT_ERROR = "INPUT_ERROR"
    SUCCESS = "SUCCESS"
    NOT_FOUND = "NOT_FOUND"


# ---------- Database Entities ---------- #
Base = declarative_base()


class Project(Base):
    __tablename__ = "project"

    # columns
    id = Column(Integer, primary_key=True)
    title: Column = Column(String(64), nullable=False)
    description: Column = Column(String(16))

    def __init__(self, title: str, description: str) -> None:
        self.title = title
        self.description = description

    def __repr__(self) -> str:
        return f"<Project(title='{self.title}', description='{self.description}')>"


class User(Base):
    __tablename__ = "user"

    # columns
    id = Column(Integer, primary_key=True)
    name: Column = Column(String(64), nullable=False)
    email: Column = Column(String(64), nullable=False, unique=True)
    password: Column = Column(String(64), nullable=False)

    def __init__(self, name: str, email: str, password: str) -> None:
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return f"<User(name='{self.name}', email='{self.email}')>"


class Issue(Base):
    __tablename__ = "issue"

    # columns
    id = Column(Integer, primary_key=True)

    # columns
    project_id: Column = Column(String(64), ForeignKey("project.id"), nullable=False)
    title: Column = Column(String(64), nullable=False)
    description: Column = Column(String(16))
    assigned_to: Column = Column(String(64), ForeignKey("user.id"))
    reported_date: Column = Column(Integer, nullable=False)
    due_date: Column = Column(Integer)
    severity: Column = Column(String(64))
    flag: Column = Column(String(16))
    tags: Column = Column(String(128))
    classification: Column = Column(String(16))
    reproducible: Column = Column(String(16))

    # relationship
    project: Project = relationship("Project")
    assigned_user: User = relationship("User")

    def __init__(
        self,
        title: str,
        project_id: str,
        description: str = None,
        assigned_to: str = None,
        due_date: int = None,
        severity: str = None,
        flag: str = None,
        tags: str = None,
        classification: str = None,
        reproducible: str = None,
    ):
        self.title = title
        self.description = description
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.reported_date = int(time.time())
        self.due_date = due_date
        self.severity = severity
        self.flag = flag
        self.tags = tags
        self.classification = classification
        self.reproducible = reproducible

    def __repr__(self) -> str:
        return f"<Issue(title='{self.title}', assigned_to='{self.assigned_to}'"


class Following(Base):
    __tablename__ = "following"

    # columns
    id = Column(Integer, primary_key=True)
    user_id = Column(String(64), ForeignKey("user.id"))
    issue_id = Column(String(64), ForeignKey("issue.id"))

    # relationship
    user: User = relationship("User")
    issue: Issue = relationship("Issue")

    def __init__(self, user_id: str, issue_id: str) -> None:
        self.user_id = user_id
        self.issue_id = issue_id

    def __repr__(self) -> str:
        return f"<Following(user_id='{self.user_id}', issue_id='{self.issue_id}')>"


class Membership(Base):
    __tablename__ = "membership"

    # columns
    id = Column(Integer, primary_key=True)
    user_id = Column(String(64), ForeignKey("user.id"))
    project_id = Column(String(64), ForeignKey("project.id"))

    # relationship
    user: User = relationship("User")
    project: Project = relationship("Project")

    def __init__(self, user_id: str, project_id: str) -> None:
        self.user_id = user_id
        self.project_id = project_id

    def __repr__(self) -> str:
        return f"<Membership(user_id='{self.user_id}', project_id='{self.project_id}')>"
