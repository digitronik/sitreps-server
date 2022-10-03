from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sitreps_server import crud
from sitreps_server import schemas
from sqlalchemy.orm import Session

from .deps import get_db

router = APIRouter()


@router.get("/")
def read_metadata(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    item = crud.metadata.get_multi(db, skip=skip, limit=limit)
    return item


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_metadata(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.MetadataCreate,
) -> Any:
    """
    Create new item.
    """
    item = crud.metadata.create(db=db, obj_in=item_in)
    return item
