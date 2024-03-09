from sqlalchemy import Column, String, Float
import csv
from database import Base

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


class url(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, nullable=False)
