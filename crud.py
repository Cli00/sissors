from fastapi import APIRouter, HTTPException, status
from schemas import usercreate, UserLogin, URLbase, urlhistory
from models import URL, USER
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
import uuid
import hashlib


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# to resister user
# @router.post("/register/", response_model=UserCreate)
class CRUDService:
    def register(self, db: Session, user_in: usercreate):
        existing_user = db.query(USER).filter(USER.email == user_in.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        user = USER(user_id=str(uuid.uuid4()), **user_in.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def authenticate_user(self, db: Session, credentials: UserLogin):
        user = db.query(USER).filter(USER.email == credentials.email).first()
        if user and user.password == credentials.password:
            return user
        return None

    def shorten(self, db: Session, url_in: URLbase):
        user_exists = db.query(USER).filter(USER.user_id == url_in.user_id).first()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
        
        hash_object = hashlib.sha256(url_in.original_url.encode())
        hex_dig = hash_object.hexdigest()[:8]
        short_url = f"domain.com/{hex_dig}"
        db_url = URL(id=str(uuid.uuid4()), **url_in.dict(), shortened_url=short_url)
        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        return db_url

    def get_user_urls(self, db: Session, user_id: urlhistory) -> List[URL]:
        return db.query(URL).filter(URL.user_id == user_id).all()






crud_service = CRUDService()