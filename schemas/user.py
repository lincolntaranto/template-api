from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    name: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    admin: bool

class UserUpdatePasswordSchema(BaseModel):
    current_password: str
    new_password: str