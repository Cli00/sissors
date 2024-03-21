from fastapi import APIRouter, HTTPException, status
from schemas import usercreate, UserLogin, URLbase, urlhistory
from models import URL, USER
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
import uuid
import hashlib
import qrcode

router = APIRouter()

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
        existing_url = db.query(URL).filter(URL.original_url == url_in.original_url).first()
        if existing_url:
            return existing_url
        
        user_exists = db.query(USER).filter(USER.user_id == url_in.user_id).first()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id")
        
        hash_object = hashlib.sha256(url_in.original_url.encode())
        hex_dig = hash_object.hexdigest()[:8]
        short_url = f"domain.com/{hex_dig}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(short_url)
        qr.make(fit=True)

        # Save QR code image to a file
        qr_image_path = f"data/{uuid.uuid4()}.png"
        qr.make_image(fill_color="black", back_color="white").save(qr_image_path)

        db_url = URL(
            id=str(uuid.uuid4()),
            user_id=url_in.user_id,
            original_url=url_in.original_url,
            shortened_url=short_url,
            qr_code_path=qr_image_path  # Store the path as a string
        )

        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        return db_url
        
    def get_url(self, db: Session, url_id: str):
        url = db.query(URL).filter(URL.id == url_id).first()  # Correct attribute access to 'db'
        return url

    def get_user_urls(self, db: Session, user_id: urlhistory) -> List[URL]:
        return db.query(URL).filter(URL.user_id == user_id).all()        
    
    def get_url_analytics_by_id(self, db: Session, url_id: str):
        url = db.query(URL).filter(URL.id == url_id).first()
        if url is None:
            return None
        
        visit_count = db.query(func.sum(URL.visit_count)).filter(URL.id == url_id).scalar()
        if visit_count is None:
            visit_count = 0
        
        return {
            "original_url": url.original_url,
            "shortened_url": url.shortened_url,
            "total_visits": visit_count,
            "created_at": url.created_at
        }
    
    def delete_url(self, db: Session, url_id: str):
        url = db.query(URL).filter(URL.id == url_id).first()
        if not url:
            return None
        db.delete(url)
        db.commit()
        return url
    
    def access_shortened_url(self, db: Session, url_id: str):
        url = db.query(URL).filter(URL.id == url_id).first()
        if url:
            url.visit_count += 1
            db.commit()
        return url

    

crud_service = CRUDService()