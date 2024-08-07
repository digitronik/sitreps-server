"""Project model."""

from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy_json import mutable_json_type

from sitreps_server.db import Base

from ..db.types import PortableJSON

if TYPE_CHECKING:
    from .jira import Jira  # noqa: F401
    from .repository import Repository  # noqa: F401


class Project(Base):
    """It represent project under ProjectGroup."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    manager_name = Column(String, index=True)
    manager_email = Column(String)
    jira_project = Column(String)

    meta = Column(mutable_json_type(dbtype=PortableJSON()))

    group_id = Column(Integer, ForeignKey("groups.id"), index=True)

    repositories = relationship("Repository", backref="project")
    jira = relationship("Jira", backref="project")
