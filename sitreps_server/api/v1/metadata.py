"""Metadata routs."""

from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from sitreps_server import crud
from sitreps_server import schemas

from .deps import get_db

router = APIRouter()


@router.get("/{repository_id}")
async def read_latest_metadata(
    *,
    db: Session = Depends(get_db),
    repository_id: int,
) -> Any:
    """Get latest metadata entry for repository."""
    item = crud.metadata.get_last_with_repository_id(db=db, repository_id=repository_id)

    if not item:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return item.meta


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_metadata(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.MetadataCreate,
) -> Any:
    """Add new metadata entry."""
    item = crud.metadata.create(db=db, obj_in=item_in)
    return item
