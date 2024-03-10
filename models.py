from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from database import Base, engine
import uuid
import csv


def read_users():
    with open("users.csv", mode='r') as file:
        reader = csv.DictReader(file)
        return [user for user in reader]

def write_users(users):
    with open("users.csv", mode='w', newline='') as file:
        fieldnames = ['first_name', 'last_name', 'email', 'password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)


class URL(Base):
    __tablename__ = "url"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

