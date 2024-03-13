from fastapi import FastAPI, HTTPException, Depends, status
from crud import crud_service
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from schemas import usercreate, UserLogin, URLbase


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return "Hello Server"

# app.include_router(router, prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/shorten/")

@app.post("/register")
def register_user(user_in: usercreate, db: Session = Depends(get_db)):
    crud_service.register(db, user_in)
    return {"message": "user successfully registered!"}

@app.post("/login")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_service.authenticate_user(db, credentials)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.user_id, "first_name": user.first_name, "last_name": user.last_name}

@app.post("/shorten")
def shorten_url(url_in:URLbase, db: Session = Depends(get_db)):
    db_url= crud_service.shorten(db, url_in)
    return {"id": db_url.id, "short_url": db_url.shortened_url}

@app.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    urls = crud_service.get_user_urls(db, user_id)
    return urls
