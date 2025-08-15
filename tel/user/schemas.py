from pydantic import BaseModel, SecretStr, EmailStr

class UserLogin(BaseModel):
    username: str
    password: SecretStr


class UserRegister(UserLogin):
    email: EmailStr


class UserUpdate(BaseModel):
    username: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    email: EmailStr | None = None
