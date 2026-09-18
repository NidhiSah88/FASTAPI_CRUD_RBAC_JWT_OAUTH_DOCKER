
from pydantic import BaseModel, EmailStr


# schemas for new users create 
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # Default role is "user"

# schemas for user login
class UserLogin(BaseModel):
    username: str
    password: str



