from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str


class UserSchema(UserCreateSchema):
    id: int
