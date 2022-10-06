from typing import TypeVar

from ..db import Base
from sitreps_server.crud.base import CRUDBase
from sitreps_server.models import CodeCoverage
from sitreps_server.schemas import CodeCoverageCreate
from sitreps_server.schemas import CodeCoverageUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDItem(CRUDBase[CodeCoverage, CodeCoverageCreate, CodeCoverageUpdate]):
    pass


code_coverage = CRUDItem(CodeCoverage)
