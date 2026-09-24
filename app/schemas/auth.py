from pydantic import BaseModel, EmailStr, Field, field_validator

class RegistrationRequest(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
    language: str | None = None

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes in UTF-8")
        return v

class RegistrationResponse(BaseModel):
    id: int
    message: str



class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 bytes in UTF-8")
        return v

class RefreshRequest(BaseModel):
    refresh_token: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"