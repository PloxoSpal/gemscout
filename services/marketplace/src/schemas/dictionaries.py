from datetime import datetime

from pydantic import BaseModel


class GemTypeRequest(BaseModel):
    name: str
    is_active: bool = True
    short_description: str | None

class GemTypeResponse(BaseModel):
    name: str
    is_active: bool
    short_description: str | None
    created_at: datetime
    updated_at: datetime