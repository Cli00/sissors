from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://scissor_test_user:pvat8pRnTK7pflWQiqb4MNyTc1fPSZbd@dpg-cno200fsc6pc73bavvc0-a/scissor_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

<<<<<<< HEAD
=======
# postgresql://postgres:blank@localhost:5432/Scissor


>>>>>>> 62219d86c06fb2e6871a6dfb25f8294ba61bc468

