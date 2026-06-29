from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.database import SessionLocal
from app.models import User
from app.schemas import (
    RegisterSchema,
    LoginSchema,
    OTPVerifySchema,
    PasswordChangeSchema,
    PasswordChangeRequestSchema
)
from app.security import hash_password, verify_password, create_token
from app.auth.otp import generate_otp, verify_otp
from app.email_service import send_email
from app.database import get_db

router = APIRouter() 



@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = User(email=data.email, password=hash_password(data.password))
    db.add(user)
    db.commit()
    return {"message": "Registration successful"}


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401)

    otp = generate_otp(user.email)
    send_email(user.email, "Login OTP", f"Your login OTP is {otp}")

    return {"message": "OTP sent to email"}



@router.post("/login/verify")
def verify_login_otp(data: OTPVerifySchema):
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400)

    token = create_token({"sub": data.email})
    return {"access_token": token}



@router.post("/password/change/request")
def password_change_request(data: PasswordChangeRequestSchema):
    otp = generate_otp(data.email)
    send_email(
        data.email,
        "Password Change OTP",
        f"Your OTP is {otp} . . Contact support if you did not request a password change."
    )
    return {"message": "OTP sent"}



@router.post("/password/change/confirm")
def password_change(data: PasswordChangeSchema, db: Session = Depends(get_db)):
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=400)

    user = db.query(User).filter(User.email == data.email).first()
    user.password = hash_password(data.new_password)
    db.commit()

    send_email(data.email, "Password Changed", "Your password was changed successfully. Please contact support if you have not authorized it.")

    return {"message": "Password updated"}





@router.get("/admin/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()