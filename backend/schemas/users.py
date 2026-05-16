from pydantic import BaseModel, ConfigDict

class UserRequestAdd(BaseModel):
    email: str
    password: str

class UserAdd(BaseModel):
    email: int
    hashed_password: str

class User(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)