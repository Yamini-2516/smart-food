# Smart Food - Campus Meal Management System

## 🍽️ Overview

Smart Food is a full-stack web application designed for campus meal management. It features user authentication, meal booking, payment processing, and admin controls for managing menus and food waste tracking.

## 🎯 Features

### Authentication System
- User Signup (Student/Guest/Admin)
- Login & Logout
- Google OAuth (Mock)
- Session management

### Dashboard
- Clean UI with navigation cards
- Daily Menu access
- Meal Booking
- Payment Management
- Feedback submission

### Meal Management
- Daily menu display (Breakfast, Lunch, Dinner)
- Admin menu updates
- Price management

### Booking System
- Student meal selection
- Date-based booking
- Confirmation system
- Guest support (lunch/dinner only)

### Payment System
- Simulated payment gateway
- UPI/Card options
- Receipt generation
- Payment tracking

### Admin Features
- Menu management
- Food waste tracking
- Analytics dashboard
- User management

### Feedback System
- Food rating (1-5 stars)
- Comments section

## 📁 Project Structure

```
smart-food/
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── menu.html
│   ├── booking.html
│   ├── payment.html
│   ├── admin.html
│   ├── feedback.html
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   └── js/
│       ├── app.js
│       ├── auth.js
│       ├── booking.js
│       ├── payment.js
│       └── admin.js
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── menu.py
│   │   ├── booking.py
│   │   ├── payment.py
│   │   ├── admin.py
│   │   └── feedback.py
│   └── database/
│       └── schema.sql
├── database/
│   └── smartfood.db
└── INSTALLATION.md
```

## 💰 Pricing

- **Breakfast**: ₹40
- **Lunch**: ₹70
- **Dinner**: ₹70

## 🚀 Installation & Setup

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite
- **Icons**: FontAwesome
- **Design**: Responsive, Modern UI/UX

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Menu
- `GET /api/menu` - Get daily menu
- `POST /api/menu` - Update menu (Admin)

### Booking
- `POST /api/book-meal` - Book meal
- `GET /api/bookings` - Get user bookings
- `GET /api/bookings/<id>` - Get booking details

### Payment
- `POST /api/payment` - Process payment
- `GET /api/payment/receipt/<id>` - Get receipt

### Admin
- `POST /api/waste-entry` - Log food waste
- `GET /api/analytics` - Get analytics data

### Feedback
- `POST /api/feedback` - Submit feedback
- `GET /api/feedback` - Get feedback (Admin)

## 👥 User Roles

- **Student**: Can book meals, make payments, provide feedback
- **Guest**: Can book lunch/dinner only, instant payment
- **Admin**: Can manage menu, track waste, view analytics

## 🔒 Security Features

- Password hashing (bcrypt)
- Session management
- CSRF protection
- Input validation

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints for tablet and desktop
- Touch-friendly buttons
- Adaptive layouts

## 🎨 Design Theme

- **Primary Color**: Green (#27AE60)
- **Secondary Color**: White (#FFFFFF)
- **Accent Color**: Orange (#E67E22)
- **Background**: Light Gray (#F5F7FA)

## 📧 Contact & Support

For issues and support, please open an issue in the repository.

## 📄 License

MIT License
