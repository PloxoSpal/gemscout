from typing import Annotated
from pydantic import BaseModel

from fastapi import Depends, Query

def PaginationParams(BaseModel):
    per_page: Annotated[int | None, Query(default=10, ge=1)]
    page: Annotated[int | None, Query(default=1, ge=1)]

PaginationDep = Annotated[PaginationParams, Depends()]




