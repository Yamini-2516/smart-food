# Installation & Setup Guide - Smart Food

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

## Backend Setup

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

Or run the schema:

```bash
sqlite3 ../database/smartfood.db < database/schema.sql
```

### Step 3: Add Sample Data

```bash
python
>>> from app import app
>>> from models import User, Meal, db
>>> with app.app_context():
>>>     # Add sample meals
>>>     db.session.add(Meal(name='Breakfast Special', meal_type='breakfast', price=40))
>>>     db.session.add(Meal(name='Lunch - Paneer Butter', meal_type='lunch', price=70))
>>>     db.session.add(Meal(name='Dinner - Dal Rice', meal_type='dinner', price=70))
>>>     db.session.commit()
>>> exit()
```

### Step 4: Run Flask Server

```bash
python app.py
```

Server will run on `http://localhost:5000`

## Frontend Setup

### Step 1: Start a Local Server

You can use Python's built-in server:

```bash
cd frontend
python -m http.server 8000
```

Or use Live Server in VS Code:
- Install Live Server extension
- Right-click on `index.html` → "Open with Live Server"

### Step 2: Access Application

- Open browser: `http://localhost:8000`
- Login page will appear
- Use test credentials:
  - **Email**: student@example.com
  - **Password**: password123

## Running the Complete Application

### Terminal 1 - Backend

```bash
cd backend
python app.py
```

### Terminal 2 - Frontend

```bash
cd frontend
python -m http.server 8000
```

### Access Application

- Frontend: `http://localhost:8000`
- API Docs: `http://localhost:5000/api/docs`

## Database Schema

The database includes the following tables:

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Meals Table
```sql
CREATE TABLE meals (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    booking_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (meal_id) REFERENCES meals(id)
);
```

### Payments Table
```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);
```

### Feedback Table
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (meal_id) REFERENCES meals(id)
);
```

### Waste Data Table
```sql
CREATE TABLE waste_data (
    id INTEGER PRIMARY KEY,
    waste_date DATE NOT NULL,
    waste_kg DECIMAL(10,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Test Credentials

### Student Account
- **Email**: student@example.com
- **Password**: password123
- **Role**: Student

### Guest Account
- **Email**: guest@example.com
- **Password**: password123
- **Role**: Guest

### Admin Account
- **Email**: admin@example.com
- **Password**: admin123
- **Role**: Admin

## Configuration

Edit `backend/config.py` to customize:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///smartfood.db'
SECRET_KEY = 'your-secret-key-here'
JWT_EXPIRATION = 86400  # 24 hours
```

## Troubleshooting

### Port Already in Use

**Error**: "Address already in use"

**Solution**:
```bash
# Change port
python app.py --port 5001
# or
python -m http.server 8001
```

### Database Errors

**Error**: "Database locked"

**Solution**:
```bash
# Delete database and reinitialize
rm database/smartfood.db
python app.py
```

### CORS Issues

The backend has CORS enabled. If you still face issues, check:
- Frontend URL in `config.py`
- Browser console for error messages

## Development Mode

For development, enable debug mode:

```python
# backend/app.py
app.run(debug=True, port=5000)
```

## Production Deployment

For production:

1. Set `DEBUG = False` in config
2. Use a production WSGI server (Gunicorn)
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS
5. Set up environment variables

## Next Steps

1. Customize the design theme in `frontend/css/style.css`
2. Add more meals to the database
3. Implement email notifications
4. Add QR code generation
5. Set up real payment gateway integration

## Support

For issues, please check:
- Browser console (F12)
- Backend logs
- Database file exists
- All dependencies installed
