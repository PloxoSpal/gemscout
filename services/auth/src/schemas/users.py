import re
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, Field

class Role(str, Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

class UserResponse(BaseModel):
    id: int
    phone: str
    role: Role
    is_2fa_enabled: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{10,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v

class UserRequest(BaseModel):
    phone: str = Field(max_length=20)

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{10,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v

class UserCreateInternal(BaseModel):

    phone: str = Field(max_length=20)

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{10,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v

