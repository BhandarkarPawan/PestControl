from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

# ---------- Database Entities ---------- #
Base = declarative_base()


class Project(Base):
    __tablename__ = "project"

    # columns
    id = Column(String(64), primary_key=True)
    title: Column = Column(String(64), nullable=False)
    description: Column = Column(String(16))

    def __init__(self, id: str, title: str, description: str):
        self.id = id
        self.title = title
        self.description = description

    def __repr__(self):
        return f"<Project(title='{self.title}', description='{self.description}')>"


class User(Base):
    __tablename__ = "user"

    # columns
    id = Column(String(64), primary_key=True)
    name: Column = Column(String(64), nullable=False)
    email: Column = Column(String(64), nullable=False)
    password: Column = Column(String(64), nullable=False)

    def __init__(self, id: str, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"


class Issue(Base):
    __tablename__ = "issue"

    # columns
    id = Column(String(64), primary_key=True)
    project_id: Column = Column(String(64), ForeignKey("project.id"))
    title: Column = Column(String(64), nullable=False)
    description: Column = Column(String(16))
    assigned_to: Column = Column(String(64), ForeignKey("user.id"))
    due_date: Column = Column(Integer, nullable=False)
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
        id: str,
        title: str,
        description: str,
        project_id: str,
        assigned_to: str,
        due_date: int,
        severity: str,
        flag: str,
        tags: str,
        classification: str,
        reproducible: str,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.due_date = due_date
        self.severity = severity
        self.flag = flag
        self.tags = tags
        self.classification = classification
        self.reproducible = reproducible

    def __repr__(self):
        return f"<Issue(title='{self.title}', assigned_to='{self.assigned_to}'"


class Following(Base):
    __tablename__ = "following"
    user_id = Column(String(64), ForeignKey("user.id"))
    issue_id = Column(String(64), ForeignKey("issue.id"))

    # relationship
    user: User = relationship("User")
    issue: Issue = relationship("Issue")

    def __init__(self, user_id: str, issue_id: str):
        self.user_id = user_id
        self.issue_id = issue_id

    def __repr__(self):
        return f"<Following(user_id='{self.user_id}', issue_id='{self.issue_id}')>"


class Membership(Base):
    __tablename__ = "membership"
    user_id = Column(String(64), ForeignKey("user.id"))
    project_id = Column(String(64), ForeignKey("project.id"))

    # relationship
    user: User = relationship("User")
    project: Project = relationship("Project")

    def __init__(self, user_id: str, project_id: str):
        self.user_id = user_id
        self.project_id = project_id

    def __repr__(self):
        return f"<Membership(user_id='{self.user_id}', project_id='{self.project_id}')>"
