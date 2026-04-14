# Event Management System - Setup Guide

## 📋 Project Overview

A modern, responsive Event Management System built with PHP, MySQL, Bootstrap 5, and SweetAlert2. The system allows:

- **Students** to browse and register for events
- **Admins** to create, manage, and approve events
- **Database-backed** user authentication and event management
- **Mobile-friendly** responsive design

## 🗄️ Database Setup

### 1. Create the Database

Before running the application, execute the SQL schema:

```bash
# Option 1: Using MySQL command line
mysql -u root -p < database_schema.sql

# Option 2: Using phpMyAdmin
# Copy the contents of database_schema.sql and run in the SQL tab
```

### 2. Database Schema

The system includes 3 main tables:

#### `users` Table
- Stores admin and student login credentials
- Default credentials (SHA256 hashed):
  - **Admin**: Username `admin`, Password `admin123`
  - **Student**: Username `student`, Password `student123`

#### `events` Table
- Stores event details (title, date, location, image, etc.)
- Status values: `Pending`, `Approved`, `Upcoming`, `Ongoing`, `Completed`, `Cancelled`
- Only events with status `Approved` or `Upcoming` are displayed to users

#### `registrations` Table
- Tracks student registrations for events
- Prevents duplicate registrations with UNIQUE constraint
- Status: `Pending`, `Approved`, `Rejected`

---

## ⚙️ Server Configuration

### Requirements

- PHP 7.4 or higher
- MySQL 5.7 or higher
- Web server (Apache/Nginx)

### Configuration File: `db_connection.php`

Update your database credentials in `db_connection.php`:

```php
$DB_HOST = 'localhost';      // Your MySQL host
$DB_NAME = 'event_management'; // Database name
$DB_USER = 'root';           // MySQL username
$DB_PASS = '';               // MySQL password
```

---

## 🚀 Default User Credentials

After running `database_schema.sql`, use these credentials to login:

### Admin Account
- **Email/Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin (Access to Admin Panel)

### Student Account
- **Email/Username**: `student`
- **Password**: `student123`
- **Role**: Student (Can view and register for events)

---

## 📁 Project Structure

```
minor_project/
├── index.php                 # Homepage with event display & login
├── profile.php               # User profile & registered events
├── logout.php                # Session logout
├── db_connection.php         # Database connection & helpers
├── database_schema.sql       # Database schema & seed data
├── style.css                 # Legacy stylesheet
├── script.js                 # Legacy scripts
├── uploads/                  # Event image uploads
├── backend/
│   ├── admin_dashboard.php   # Admin main dashboard
│   ├── student_dashboard.php # Student dashboard
│   ├── create_event_handler.php  # Event creation logic
│   ├── admin_pages/
│   │   ├── dashboard.php     # Dashboard overview
│   │   ├── event_management.php
│   │   ├── create_event.php
│   │   ├── registrations.php
│   │   ├── analytics.php
│   │   └── settings.php
│   └── admin_dashboard.css   # Admin panel styling
└── assets/
    ├── css/
    │   └── admin_dashboard.css
    └── js/
        └── admin_dashboard.js
```

---

## 🔐 Key Features

### 1. **Homepage (index.php)**
- Responsive navbar with navigation links
- Hero section with event showcase
- Upcoming events grid display
- Dual login modal (Student/Admin)
- SweetAlert2 notifications
- Join event functionality with database tracking

### 2. **Authentication**
- Session-based login system
- Supports both SHA256 and bcrypt passwords
- Role-based redirects (Admin → Admin Panel, Student → Profile)

### 3. **Event Registration**
- Students can join events with one click
- Prevents duplicate registrations (UNIQUE constraint)
- Real-time success/error feedback
- Registration status tracking

### 4. **Admin Panel**
- Create and manage events
- Approve/reject event registrations
- View event analytics
- User management
- Image upload for events

### 5. **User Profile**
- View registered events
- Check registration status
- Account information display

---

## 🎨 Design Features

### Colors & Gradients
- **Primary**: Purple gradient (`#667eea` → `#764ba2`)
- **Secondary**: Pink gradient (`#f093fb` → `#f5576c`)
- Clean, modern card-based UI
- Mobile-first responsive design

### UI Components
- Bootstrap 5 framework
- Font Awesome 6 icons
- SweetAlert2 for notifications
- Smooth animations & transitions
- Hover effects on cards

---

## 🔧 API Endpoints

### Login
```
POST /index.php
Parameters:
  - action: "login"
  - role: "admin" or "student"
  - identity: email or username
  - password: user password

Response: JSON
{
  "success": true/false,
  "message": "...",
  "role": "admin|student"
}
```

### Register for Event
```
POST /index.php
Parameters:
  - action: "register_event"
  - event_id: event ID

Response: JSON
{
  "success": true/false,
  "message": "..."
}
```

---

## 🛡️ Security Features

- **Prepared Statements**: All SQL queries use PDO prepared statements
- **Password Hashing**: SHA256 hashing in seed data, bcrypt support for new passwords
- **Session Management**: Secure session handling with authentication checks
- **Input Validation**: All user inputs are validated and sanitized
- **HTML Escaping**: XSS prevention with `htmlspecialchars()`

---

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

All pages are fully responsive and optimized for mobile devices.

---

## 🧪 Testing Credentials

### Quick Test Flow:

1. **Navigate to index.php**
2. **Click "Login / Signup"** button
3. **Student Login Tab:**
   - Username: `student`
   - Password: `student123`
4. **Click "Join Event"** button
5. **See success confirmation** via SweetAlert2
6. **View registered events** in profile

### Admin Test Flow:

1. **Navigate to index.php**
2. **Click "Login / Signup"** button
3. **Switch to "Admin Login"** tab
4. **Admin Email/Username**: `admin`
5. **Password**: `admin123`
6. **Redirected to Admin Panel** for event management

---

## ⚠️ Troubleshooting

### Issue: "Database connection failed"
**Solution**: Check `db_connection.php` credentials against your MySQL setup

### Issue: Events not displaying
**Solution**: Ensure events have status `Approved` or `Upcoming` in the database

### Issue: Login fails
**Solution**: Verify credentials in `users` table using phpMyAdmin

### Issue: Images not uploading
**Solution**: Ensure `uploads/` folder exists with write permissions (chmod 755)

---

## 🔄 Future Enhancements

- Email notifications for event registration
- Payment gateway integration for paid events
- Event categories and advanced filtering
- User reviews and ratings
- Multi-language support
- Two-factor authentication

---

## 📞 Support

For issues or questions regarding the setup, please check:
1. Database credentials in `db_connection.php`
2. Database schema execution
3. Server permissions for file uploads
4. PHP version compatibility

---

**Last Updated**: April 2026
