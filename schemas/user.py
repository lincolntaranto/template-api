from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateSchema(BaseModel):
    name: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    admin: bool

class UserUpdatePasswordSchema(BaseModel):
    current_password: str
    new_password: str

class NewPassword(BaseModel):
    token: str
    new_password: str

class UserUpdateEmailSchema(BaseModel):
    new_email: EmailStr
    current_password: str

class UserUpdateNameSchema(BaseModel):
    new_name: str
    current_password: str

class DeleteAccountSchema(BaseModel):
    current_password: str