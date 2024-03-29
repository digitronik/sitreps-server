from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_first(self, db: Session) -> Optional[ModelType]:
        return db.query(self.model).first()

    def get_with_project_id(self, db: Session, project_id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.project_id == project_id).first()

    def get_service_with_name_env(self, db: Session, service: Any, env: Any) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.service == service, self.model.env == env)
            .first()
        )

    def get_services_with_name_env(
        self, db: Session, service: Any, env: Any
    ) -> Optional[ModelType]:
        return (
            db.query(self.model).filter(self.model.service == service, self.model.env == env).all()
        )

    def get_with_repository_id(self, db: Session, repository_id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.repository_id == repository_id).first()

    def get_last_with_project_id(self, db: Session, project_id: Any) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.project_id == project_id)
            .order_by(self.model.time.desc())
            .first()
        )

    def get_last_with_repository_id(self, db: Session, repository_id: Any) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.repository_id == repository_id)
            .order_by(self.model.time.desc())
            .first()
        )

    def get_last_req_portal_avg(
        self, db: Session, plugin: Any, avg: Any, env: Any
    ) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.plugin == plugin)
            .filter(self.model.avg == avg)
            .filter(self.model.env == env)
            .order_by(self.model.time.desc())
            .first()
        )

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, filters: dict = None
    ) -> List[ModelType]:
        # return db.query(self.model).offset(skip).limit(limit).all()
        quary = db.query(self.model)
        if filters:
            for key, value in filters.items():
                quary = quary.filter(getattr(self.model, key) == value)
        return quary.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
