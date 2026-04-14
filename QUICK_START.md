# ⚡ QUICK START - Event Management System

## 🎯 Your Files Are Ready!

✅ **`index_new.php`** - Complete all-in-one application  
✅ **`schema.sql`** - Database setup with sample data  
✅ **`VS_CODE_SETUP.md`** - Full setup guide

---

## 🚀 5-Minute Quick Start

### 1. Start XAMPP
```
- Open XAMPP Control Panel
- Click "Start" for Apache
- Click "Start" for MySQL
- Wait for green lights
```

### 2. Create Database
```
- Open: http://localhost/phpmyadmin
- Click "New" → Type "event_management"
- Click "Create"
- Go to SQL tab
- Paste contents of schema.sql
- Click "Go"
```

### 3. Copy Your File
```
- Go to: C:\xampp\htdocs\
- Create folder: event_management
- Copy index_new.php here
- Rename to: index.php
```

### 4. Open in Browser
```
http://localhost/event_management/index.php
```

### 5. Test the Features
```
Login: student@example.com / student123
OR
     admin@example.com / admin123

Try joining an event! 🎉
```

---

## 🔑 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| **Student** | `student@example.com` | `student123` |
| **Admin** | `admin@example.com` | `admin123` |

---

## ✨ Features Working!

✅ Modern UI (Purple gradient header)  
✅ Login/Signup system (3 tabs)  
✅ Event browsing (10 sample events)  
✅ Join event button (with smart logic)  
✅ Student registration  
✅ SweetAlert2 notifications  
✅ Session management  
✅ Admin panel access  
✅ Mobile responsive  
✅ Database integrated  

---

## 📋 Join Event Logic

### When NOT logged in:
- Click "Join Event" → **Login modal appears automatically** ✓

### When logged in as Student:
- Click "Join Event" → **Saved to database** ✓
- Button changes to "✓ Joined" ✓
- Success notification appears ✓

### When logged in as Admin:
- Shows "Manage Event" button instead ✓
- Can access admin dashboard ✓

---

## 🎨 What You Get

### UI/UX
- Professional purple/blue gradient header
- Clean white event cards
- Responsive 3-column grid (mobile-friendly)
- Smooth animations & transitions
- Font Awesome icons

### Authentication
- Dual login tabs (Student/Admin)
- Sign up form with validation
- Bcrypt password hashing
- Session management
- Logout with confirmation

### Database
- MySQL integration (PDO)
- 3 tables: users, events, registrations
- 10 sample events included
- Prepared statements (secure)
- Foreign keys & constraints

### API
- AJAX login/signup (no page reload)
- Event registration API
- JSON responses
- Error handling

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **Can't connect to localhost** | Start MySQL in XAMPP |
| **Events not showing** | Run schema.sql in phpMyAdmin |
| **Login not working** | Check database has users table |
| **File not found** | Verify path: `C:\xampp\htdocs\event_management\index.php` |
| **Button clicks not working** | Check browser console (F12) for errors |

---

## 📝 Full Details

For complete setup instructions, see: **VS_CODE_SETUP.md**

---

## 💾 All-in-One File Benefits

✨ **Single PHP file** (no config files needed)  
✨ **Includes HTML, CSS, JavaScript, PHP** (everything in one!)  
✨ **Ready to deploy** (works on any PHP server)  
✨ **Easy to customize** (modify code anywhere in file)  
✨ **Perfect for learning** (see all components together)  

---

## 🎯 Next: Follow the 5-Minute Setup Above!

Once done, you'll have:
- ✅ Professional event management system
- ✅ Working login/signup
- ✅ Event browsing & joining
- ✅ Student registrations saved in database
- ✅ Admin controls available

**Let's go! 🚀**

---

**Questions?** Check VS_CODE_SETUP.md for detailed instructions!
