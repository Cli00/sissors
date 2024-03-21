# FastAPI Project README

## Overview
This FastAPI project provides a registration and login system using SQLAlchemy for database interaction and Jinja2Templates for rendering HTML templates.(error error error) sorry

## Features
- User registration with email validation
- User authentication and login
- URL Shortening: Scissor allow users to shorten URLs by pasting a long URL into the Scissor platform and a shorter URL gets automatically generated.
- QR Code Generation: Scissor allows users to also generate QR codes for the shortened URLs. Users can download the QR code image and use it in their promotional materials or/and on their website.
- Analytics: Scissor provides basic analytics that allows users to track their shortened URL’s performance. Users can see how many clicks their shortened URL has received.
– Link History: Scissor allows users to see the history of links they’ve created so they can easily find and reuse links they have previously created

## Project Structure
- `main.py`: Contains the FastAPI application setup and endpoint definitions.
- `database.py`: Handles database setup and connection.
- `models.py`: Defines SQLAlchemy models for database tables.
- `crud.py`: contatn the functions
- `schemas.py`: 
- `requirements.txt`: List of Python dependencies.
- 
## Usage
1. Register a new user by accessing `/register` endpoint.
2. Login with registered credentials at `/login` endpoint.
3. Shorten your url by inputing your user_id at `/shorten` endpoint.
4. Increase your visit count by inputing your url_id in Visit Original Url at `/redirect/{url_id}` endpoint.
5. Get your hystory by inputing user_id at `/history/{user_id}` endpoint.
6. Get your Url Analytics By inputing your User Id at `/analytics/id/{url_id}` endpoint.
7. Get Your Url Qr Code By inputing your url Id at `/qr_code/{url_id}` endpoint.
8. To registered Delete Url at `/history/{url_id}` endpoint.

## Dependencies
- FastAPI
- SQLAlchemy
- Jinja2
- Uvicorn

## Contributors
- clinton shaibu <clintonidegu@gmail.com>

## License
This project is a test work for development - see the `LICENSE` file for details.
