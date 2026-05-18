import re

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    EmailStr,
    PastDate
)

class UserRequestAdd(BaseModel):

    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    phone: str = Field(max_length=20)
    password: str = Field(max_length=255)
    date_of_birth: PastDate
    country: str = Field(max_length=255)
    city: str = Field(max_length=255)
    organization: str = Field(max_length=255)
    address: str = Field(max_length=255)
    experience_years: int = Field(max_digits=80)

    profile_image: str | None
    passport_photo: str | None

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{10,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v

class UserAdd(BaseModel):
    email: int
    hashed_password: str

class User(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)