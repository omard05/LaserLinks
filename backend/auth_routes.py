from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from auth_utils import codes_match, generate_code, hash_code, is_ivc_email
from database import get_db
from models import EmailCode, User

router = APIRouter(prefix="/auth", tags=["auth"])

CODE_LIFETIME = timedelta(minutes=10)
MAX_ATTEMPTS = 5


class RequestCodeIn(BaseModel):
    name: str
    email: str


class VerifyCodeIn(BaseModel):
    email: str
    code: str


@router.post("/request-code")
def request_code(data: RequestCodeIn, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if not is_ivc_email(email):
        raise HTTPException(status_code=400, detail="Use your @ivc.edu email.")

    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(name=data.name.strip(), email=email)
        db.add(user)

    db.execute(delete(EmailCode).where(EmailCode.email == email))

    code = generate_code()
    db.add(
        EmailCode(
            email=email,
            code_hash=hash_code(code),
            expires_at=datetime.now(timezone.utc) + CODE_LIFETIME,
        )
    )
    db.commit()

    print(f"[DEV] Verification code for {email}: {code}", flush=True)
    return {"message": "Code sent."}

@router.post("/verify")
def verify_code(data: VerifyCodeIn, db: Session = Depends(get_db)):
    # 1. Clean the email (same as request_code)
    email = data.email.strip().lower()

    # 2. Find the EmailCode row for this email
    #    Hint: same pattern as finding the user in request_code, but select EmailCode
    record = db.scalar(select(EmailCode).where(EmailCode.email == email))

    # 3. If no row was found -> raise HTTPException 400, "No code requested."
    if not record:
        raise HTTPException(status_code=400, detail="No code requested.")

    # 4. If the code is expired -> delete the row, commit, raise 400 "Code expired."
    #    Hint: compare datetime.now(timezone.utc) to record.expires_at
    if datetime.now(timezone.utc) > record.expires_at:
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="Code expired.")

    # 5. If attempts >= MAX_ATTEMPTS -> raise HTTPException 429, "Too many attempts. Request a new code."
    if record.attempts >= MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many attempts. Request a new code.")

    # 6. If the code is wrong -> add 1 to record.attempts, commit, raise 400 "Wrong code."
    #    Hint: use your codes_match(code, stored_hash) function
    if not codes_match(data.code.strip(), record.code_hash):
        record.attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Wrong code.")

    # 7. Success: find the user, set user.verified = True,
    #    delete the code row, commit, return {"verified": True}
    user = db.scalar(select(User).where(User.email == email))
    user.verified = True
    db.delete(record)
    db.commit()
    return {"verified": True}