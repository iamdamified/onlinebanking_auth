from pydantic import BaseModel, EmailStr, field_validator

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class OTPVerifySchema(BaseModel):
    email: EmailStr
    otp: str

class PasswordChangeRequestSchema(BaseModel):
    email: EmailStr

class PasswordChangeSchema(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, info):
        new_password = info.data.get("new_password")
        if new_password and confirm_password != new_password:
            raise ValueError("Passwords do not match")
        return confirm_password