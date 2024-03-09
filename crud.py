import hashlib
import uuid
from fastapi import APIRouter, HTTPException, status
from schemas import URLbase, UserCreate, UserLogin
from models import read_users, url, write_users
from sqlalchemy.orm import Session

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

@router.post("/shorten/")
def shorten_url(long_url):
    hash_object = hashlib.sha256(long_url.encode())
    hex_dig = hash_object.hexdigest()
    short_url = hex_dig[:8] 
    return {"shortened_url": f"domain.com/{short_url}"}

# @router.get("/retrieve/{short_id}")
# async def get_original_url(self, short_id: str, db: Session):
#     # Retrieve URL object from session using the short ID
#     url_data = db.query(URLSerializer).filter_by(id=short_id).first()
#     if url_data:
#         return {"original_url": url_data.original_url}
#     else:
#         raise HTTPException(status_code=404, detail="URL not found")

