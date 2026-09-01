from pydantic import BaseModel, EmailStr, Field

class UserRegistration(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
    language: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RegistrationResponse(BaseModel):
    id: int
    message: str