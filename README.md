# FastAPI Project README

## Overview
This FastAPI project provides a registration and login system using SQLAlchemy for database interaction and Jinja2Templates for rendering HTML templates.

## Features
- User registration with email validation
- User authentication and login
- URL Shortening: Scissor allow users to shorten URLs by pasting a long URL into the Scissor platform and a shorter URL gets automatically generated.
- QR Code Generation: Scissor allows users to also generate QR codes for the shortened URLs. Users can download the QR code image and use it in their promotional materials or/and on their website.
- Analytics: Scissor provides basic analytics that allows users to track their shortened URL’s performance. Users can see how many clicks their shortened URL has received.
– Link History: Scissor allows users to see the history of links they’ve created so they can easily find and reuse links they have previously created

## Setup
1. Install dependencies using `pip install -r requirements.txt`
2. Run the development server using `uvicorn main:app --reload`
3. Access the application at `http://localhost:8000`

## Project Structure
- `main.py`: Contains the FastAPI application setup and endpoint definitions.
- `database.py`: Handles database setup and connection.
- `models.py`: Defines SQLAlchemy models for database tables.
- `templates/`: Directory containing HTML templates used for rendering.(had errors so pass)
- `requirements.txt`: List of Python dependencies.

## Usage
1. Register a new user by accessing `/register` endpoint.
2. Login with registered credentials at `/login` endpoint.
3. Access the dashboard at `/dashboard` after successful login.

## Dependencies
- FastAPI
- SQLAlchemy
- Jinja2
- Uvicorn

## Contributors
- John Doe <johndoe@example.com>
- Jane Smith <janesmith@example.com>

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
