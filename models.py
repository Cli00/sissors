from sqlalchemy import Column, String
from database import Base, engine

class USER(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

class URL(Base):
    __tablename__ = "url"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

