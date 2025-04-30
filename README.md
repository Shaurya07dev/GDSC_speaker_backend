# Speaker Booking Backend

A Flask-based backend API for a speaker booking system that allows users to book speakers for events.

## Features

- User registration and authentication
- Email verification with OTP
- Speaker profile management
- Booking management
- Role-based access control (Speaker/Organizer)

## Prerequisites

- Python 3.8 or higher
- Git
- Gmail account (for email functionality)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd speaker-booking-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///app.db
   JWT_SECRET_KEY=your-jwt-secret-key
   MAIL_USERNAME=your-gmail@gmail.com
   MAIL_PASSWORD=your-gmail-app-password
   ```

   Note: For Gmail, you need to:
   - Enable 2-Step Verification
   - Generate an App Password
   - Use the App Password as MAIL_PASSWORD

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/verify-otp` - Verify email with OTP

### Speakers
- `GET /speakers/me` - Get speaker profile
- `POST /speakers/profile` - Update speaker profile

### Users
- `GET /users/speakers` - List all speakers

### Bookings
- `POST /bookings` - Create a new booking
- `GET /bookings` - List bookings
- `GET /bookings/<id>` - Get booking details
- `PUT /bookings/<id>` - Update booking status

## Example Usage

1. **Register a new user**
   ```bash
   curl -X POST http://127.0.0.1:5000/auth/register \
   -H "Content-Type: application/json" \
   -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "password": "password123",
       "user_type": "speaker"
   }'
   ```

2. **Verify email with OTP**
   ```bash
   curl -X POST http://127.0.0.1:5000/auth/verify-otp \
   -H "Content-Type: application/json" \
   -d '{
       "email": "john@example.com",
       "otp": "123456"
   }'
   ```

3. **Login**
   ```bash
   curl -X POST http://127.0.0.1:5000/auth/login \
   -H "Content-Type: application/json" \
   -d '{
       "email": "john@example.com",
       "password": "password123"
   }'
   ```

## Project Structure

```
speaker-booking-backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── speakers.py
│   │   ├── users.py
│   │   └── bookings.py
│   ├── utils/
│   │   ├── email.py
│   │   └── otp.py
│   └── middleware.py
├── migrations/
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
```
