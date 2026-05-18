from pydantic import BaseModel

from typing import TypeVar, Generic
from src.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)

class DataMapper(Generic[SchemaType, ModelType]):
    db_model: type[ModelType]
    schema: type[SchemaType]

    @classmethod
    def to_schema(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def to_model(cls, data):
        return cls.db_model(**data.model_dump())





