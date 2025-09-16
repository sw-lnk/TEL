from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from sqlmodel import Relationship

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_active: bool = False


class UserShort(SQLModel):
    first_name: str
    last_name: str
    

class UserProfile(UserBase, UserShort):
    email: EmailStr = Field(default=None, unique=True, index=True)
    is_superuser: bool = False
    

class User(UserProfile, table=True):    
    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str
    
    messages: list["Message"] = Relationship(back_populates="user")  # type: ignore # noqa: F821
