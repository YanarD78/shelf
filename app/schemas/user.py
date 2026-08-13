from pydantic import BaseModel, EmailStr, Field

class UserRegistration(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RegistrationResponse(BaseModel):
    id: int
    message: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str