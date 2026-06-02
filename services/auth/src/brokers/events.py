from datetime import datetime, timezone

from pydantic import BaseModel, Field

USER_REGISTERED = "user.registered"

class UserRegisteredEvent(BaseModel):
    user_id: int
    phone_number: str
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))