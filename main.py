from fastapi import FastAPI, Form, HTTPException, Depends, status
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import EmailStr
from crud import crud_service
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import usercreate, UserLogin, URLbase
from fastapi.templating import Jinja2Templates



# Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return "Hello Server"

@app.post("/register", response_class=HTMLResponse)
def register_user(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user_in = usercreate(first_name=first_name, last_name=last_name, email=email, password=password)
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


@app.get("/analytics/id/{url_id}")
def get_url_analytics_by_id(url_id: str, db: Session = Depends(get_db)):
    analytics_data = crud_service.get_url_analytics_by_id(db, url_id)
    if analytics_data is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return analytics_data

@app.get("/qr_code/{url_id}")
def get_qr_code(url_id: str, db: Session = Depends(get_db)):
    url = crud_service.get_url(db, url_id)  # Call get_url method from CRUDService
    
    if url:
        if url.qr_code_path:
            return FileResponse(url.qr_code_path)
        else:
            raise HTTPException(status_code=404, detail="QR code not found")
    else:
        raise HTTPException(status_code=404, detail="URL not found")
    
@app.delete("/history/{url_id}")
def delete_url(url_id: str, db: Session = Depends(get_db)):
    url = crud_service.delete_url(db, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"message": "URL deleted successfully"}

@app.get("/redirect/{url_id}")
def redirect_to_original_url(url_id: str, db: Session = Depends(get_db)):
    url = crud_service.access_shortened_url(db, url_id)
    
    if url:
        return {"original_url": url.original_url}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    
