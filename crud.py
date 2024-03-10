from fastapi import APIRouter, HTTPException, status
from schemas import UserCreate, UserLogin
from models import URL, read_users, write_users
from database import SessionLocal
import hashlib


router = APIRouter()

# to resister user
@router.post("/register/", response_model=UserCreate)
async def register(user: UserCreate):
    users = read_users()

    # Check if the email is already registered
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # If not, add the new user and write to CSV
    users.append(user.dict())
    write_users(users)
    return user


# login to user
@router.post("/login/")
async def login(user: UserLogin):
    users = read_users()

    for stored_user in users:
        if (
            stored_user["email"] == user.email
            and stored_user["password"] == user.password
        ):
            return {"message": "Login successful"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/shorten/")
def shorten_url(long_url):
    hash_object = hashlib.sha256(long_url.encode())
    hex_dig = hash_object.hexdigest()[:8]
    short_url = f"domain.com/{hex_dig}"

    db = SessionLocal()
    db_url = URL(original_url=long_url, shortened_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db.close()

    return {"id": db_url.id, "original_url": db_url.original_url, "shortened_url": db_url.shortened_url}

@router.get("/retrieve/{url_id}")
def retrieve_url(url_id: str):
    db = SessionLocal()
    db_url = db.query(URL).filter(URL.id == url_id).first()
    if db_url:
        return {"original_url": db_url.original_url, "shortened_url": db_url.shortened_url}
    raise HTTPException(status_code=404, detail="URL not found")


