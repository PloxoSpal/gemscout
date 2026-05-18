import re

from pydantic import BaseModel, Field, field_validator

class ResponseAuthCode(BaseModel):
    phone: str
    code: int

    @field_validator('phone')
    @classmethod
    def validate_phone_number(cls, v):
        pattern = r'^\+?[1-9]\d{10,14}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number')
        return v