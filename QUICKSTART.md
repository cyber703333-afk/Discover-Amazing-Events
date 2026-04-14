# 🚀 Quick Start Guide - Event Management System

## Step 1: Setup Python Virtual Environment

### On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.2
- Werkzeug 2.3.6
- SQLAlchemy 2.0.19

## Step 3: Run the Application
```bash
python app.py
```

### Expected Output:
```
✅ Database initialized with default users!
Admin: admin@example.com / admin123
Student: student@example.com / student123

🚀 Starting Event Management System...
📝 Access the application at: http://127.0.0.1:5000
```

## Step 4: Access the Application
- Open your browser and go to: **http://127.0.0.1:5000**
- The homepage loads automatically
- Use the login/register buttons in the navbar

## 👥 Default Login Credentials

### Student Account
```
Email: student@example.com
Password: student123
```

### Admin Account
```
Email: admin@example.com
Password: admin123
```

## 📁 Project Structure Created

```
templates/
├── base.html              ✅ Master template
├── index.html             ✅ Home page
├── login.html             ✅ Login page
├── register.html          ✅ Registration
├── event_details.html     ✅ Event details
├── my_events.html         ✅ My events
├── admin/                 ✅ Admin folder
│   ├── admin_dashboard.html
│   ├── create_event.html
│   ├── manage_events.html
│   ├── edit_event.html
│   ├── manage_registrations.html
│   └── manage_users.html
└── errors/                ✅ Error pages
    ├── 403.html
    ├── 404.html
    └── 500.html

static/uploads/           ✅ For event images

app.py                    ✅ Main Flask app
requirements.txt          ✅ Dependencies
event_management.db       ✅ SQLite database (auto-created)
```

## 🎯 Testing the Application

### As a Student:
1. Click **Login** → Select **Student Tab**
2. Enter: `student@example.com` / `student123`
3. Browse events on homepage
4. Click **View Details** on any event
5. Click **Join Event** to register
6. Go to **My Events** to see registrations

### As an Admin:
1. Click **Login** → Select **Admin Tab**
2. Enter: `admin@example.com` / `admin123`
3. You're auto-redirected to **Admin Dashboard**
4. Create new events
5. Manage existing events
6. View registrations and users

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Virtual Environment Issues
```bash
# Deactivate first
deactivate

# Delete and recreate venv
rmdir venv  # or rm -rf venv on macOS/Linux
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
```

### Module Not Found Errors
```bash
# Make sure venv is activated, then reinstall
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Delete database and reinitialize
rm event_management.db
python app.py
```

## 📝 File Upload Notes

- Supports: PNG, JPG, JPEG, GIF, WebP
- Max size: 5MB
- Location: `static/uploads/`
- Files are automatically renamed for security

## 🔐 Security Features

✅ Password hashing with Werkzeug
✅ SQL injection prevention (SQLAlchemy ORM)
✅ Secure file upload handling
✅ Admin-only route protection
✅ User session management

## 📊 Database Models

The system creates 3 main tables:

1. **users** - Student/Admin accounts
2. **events** - Event details and metadata
3. **registrations** - User-Event relationships

All relationships are properly configured with cascading deletes.

## 🎨 Frontend Features

- Bootstrap 5 responsive design
- Purple/Blue gradient theme
- SweetAlert2 notifications
- Font Awesome icons
- Mobile-friendly interface
- Real-time search filters
- Progressive enhancement

## 🚨 Deactivating Virtual Environment

When done, deactivate the virtual environment:
```bash
deactivate
```

---

## ✨ Next Steps

1. **Customize Users:** Modify admin/student credentials in `init_db()` function
2. **Add Sample Events:** Create events through admin dashboard
3. **Deploy:** See README.md for production deployment guide
4. **Configure:** Edit settings in `app.py` config section

---

**Happy Coding!** 🎉

Need help? Check the full README.md for detailed documentation.
