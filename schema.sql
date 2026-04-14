-- ============================================================
-- EVENT MANAGEMENT SYSTEM - SQL SCHEMA
-- ============================================================
-- Copy & paste this entire script into phpMyAdmin SQL tab
-- Or run: mysql -u root -p < schema.sql
-- ============================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS event_management;
USE event_management;

-- ============================================================
-- USERS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role ENUM('admin', 'student') NOT NULL DEFAULT 'student',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email (email),
  INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- EVENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(100) DEFAULT 'General',
  event_date DATE NOT NULL,
  event_time TIME,
  location VARCHAR(255),
  image VARCHAR(255),
  organizer VARCHAR(150),
  max_participants INT DEFAULT 0,
  status ENUM('Pending', 'Approved', 'Upcoming', 'Ongoing', 'Completed', 'Cancelled') DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_date (event_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- REGISTRATIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS registrations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_registration (user_id, event_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  INDEX idx_user (user_id),
  INDEX idx_event (event_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- SEED DATA - DEFAULT USERS
-- ============================================================
-- Admin credentials: admin@example.com / admin123
-- Student credentials: student@example.com / student123
-- ============================================================

INSERT INTO users (name, email, password, role) VALUES
(
  'Admin User',
  'admin@example.com',
  '$2y$10$k2K0mVMf7wKpDJ3wK0wK2OzK0mVMf7wKpDJ3wK0wK2',  -- Password: admin123 (bcrypt)
  'admin'
),
(
  'Student User',
  'student@example.com',
  '$2y$10$6DY.6scCXbJ0Wc9wK0mK2OzK0mVMf7wKpDJ3wK0wK2', -- Password: student123 (bcrypt)
  'student'
);

-- ============================================================
-- SEED DATA - SAMPLE EVENTS
-- ============================================================

INSERT INTO events (title, description, category, event_date, event_time, location, organizer, max_participants, status) VALUES
(
  'Tech Conference 2026',
  'Join us for an amazing tech conference featuring industry leaders discussing the latest trends in AI, Cloud Computing, and Web Development.',
  'Technology',
  '2026-05-15',
  '09:00:00',
  'Convention Center, Downtown',
  'Tech Society',
  500,
  'Approved'
),
(
  'Summer Music Festival',
  'Experience three days of live music performances from local and international artists. Food, drinks, and entertainment all in one place!',
  'Music',
  '2026-06-20',
  '18:00:00',
  'Central Park',
  'Entertainment Plus',
  5000,
  'Approved'
),
(
  'Web Development Workshop',
  'Learn modern web development with hands-on coding sessions. Topics include HTML, CSS, JavaScript, React, and Node.js.',
  'Education',
  '2026-04-10',
  '10:00:00',
  'Tech Hub Training Center',
  'Code Academy',
  50,
  'Approved'
),
(
  'Business Networking Event',
  'Connect with entrepreneurs, investors, and business professionals. Share ideas and build partnerships in a relaxed setting.',
  'Business',
  '2026-05-05',
  '17:00:00',
  'Grand Hotel Grand Ballroom',
  'Business League',
  200,
  'Approved'
),
(
  'Hackathon 2026',
  'A 24-hour coding competition where teams build innovative solutions. Win prizes worth $50,000 and gain recognition!',
  'Technology',
  '2026-07-01',
  '08:00:00',
  'Tech Innovation Labs',
  'Dev Community',
  300,
  'Approved'
),
(
  'Photography Exhibition',
  'Showcase of stunning photography from around the world. Open to public. Free entry with light refreshments.',
  'Art',
  '2026-04-25',
  '11:00:00',
  'Art Gallery Downtown',
  'Photography Club',
  100,
  'Approved'
),
(
  'Marathon 2026',
  'Annual city marathon featuring 5K and 10K categories. Great for fitness enthusiasts and charity supporters.',
  'Sports',
  '2026-05-30',
  '06:00:00',
  'City Stadium & Routes',
  'Sports Association',
  2000,
  'Approved'
),
(
  'Entrepreneurship Summit',
  'Learn from successful entrepreneurs about starting and scaling your business. Includes mentorship sessions.',
  'Business',
  '2026-06-10',
  '09:00:00',
  'Business Center Tower',
  'Startup Foundation',
  400,
  'Approved'
),
(
  'AI & Machine Learning Bootcamp',
  'Intensive 5-day bootcamp covering fundamentals of AI, ML, Neural Networks, and practical applications.',
  'Education',
  '2026-05-20',
  '14:00:00',
  'Tech Institute',
  'ML Academy',
  30,
  'Approved'
),
(
  'Art & Design Expo',
  'Interactive exhibition featuring digital art, graphic design, and creative works. Meet designers and get inspired!',
  'Art',
  '2026-06-15',
  '12:00:00',
  'Convention Hall',
  'Creative Collective',
  500,
  'Approved'
);

-- ============================================================
-- QUERY TO VERIFY SETUP
-- ============================================================
-- SELECT 'Users' as table_name, COUNT(*) as count FROM users
-- UNION ALL
-- SELECT 'Events', COUNT(*) FROM events
-- UNION ALL
-- SELECT 'Registrations', COUNT(*) FROM registrations;
