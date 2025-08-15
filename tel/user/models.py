from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_active: bool = False


class UserProfile(UserBase):
    email: EmailStr = Field(default=None, unique=True)
    is_superuser: bool = False
    

class User(UserProfile, table=True):    
    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str
