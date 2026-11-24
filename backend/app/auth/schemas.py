from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    display_name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    password_confirmation: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class ChallengeRequest(BaseModel):
    email: EmailStr


class ChallengeConfirmRequest(BaseModel):
    token: str = Field(min_length=32, max_length=256)


class PasswordResetRequest(BaseModel):
    token: str = Field(min_length=32, max_length=256)
    password: str = Field(min_length=12, max_length=128)
    password_confirmation: str = Field(min_length=12, max_length=128)


class ProfileUpdateRequest(BaseModel):
    display_name: str = Field(min_length=2, max_length=80)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=12, max_length=128)
    new_password: str = Field(min_length=12, max_length=128)
    new_password_confirmation: str = Field(min_length=12, max_length=128)
