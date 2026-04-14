"""
Event Management System - Flask Application
Modern, Professional, Scalable Python Web Application
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

# ============================================================
# FLASK APP INITIALIZATION
# ============================================================

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ============================================================
# DATABASE MODELS
# ============================================================

class User(UserMixin, db.Model):
    """User Model - Students and Admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # admin or student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('Registration', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.email}>'


class Event(db.Model):
    """Event Model"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), default='General')
    date = db.Column(db.DateTime, nullable=False, index=True)
    venue = db.Column(db.String(255))
    image_filename = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending or success
    organizer = db.Column(db.String(150))
    max_participants = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def registration_count(self):
        """Get count of registrations for this event"""
        return len(self.registrations)
    
    def is_user_registered(self, user_id):
        """Check if user is registered for this event"""
        return Registration.query.filter_by(user_id=user_id, event_id=self.id).first() is not None
    
    def get_registration_count(self):
        """Get count of registered users for this event"""
        return Registration.query.filter_by(event_id=self.id, status='registered').count()
    
    __repr__ = lambda self: f'<Event {self.title}>'


class Registration(db.Model):
    """Event Registration Model"""
    __tablename__ = 'registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_registration'),)
    
    __repr__ = lambda self: f'<Registration {self.user_id} -> {self.event_id}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    return User.query.get(int(user_id))

# ============================================================
# DECORATORS
# ============================================================

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin rights required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================
# HELPER FUNCTIONS
# ============================================================

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload_file(file):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to make it unique
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

@app.template_filter('event_image_url')
def event_image_url(image_filename):
    if not image_filename:
        return None
    if image_filename.startswith(('http://', 'https://', '/')):
        return image_filename
    return url_for('static', filename=f'uploads/{image_filename}')

@app.template_filter('is_pdf')
def is_pdf(filename):
    return bool(filename and filename.lower().endswith('.pdf'))

# ============================================================
# CONTEXT PROCESSORS
# ============================================================

@app.context_processor
def inject_user():
    """Make current_user available in all templates"""
    return {'current_user': current_user}

# ============================================================
# ROUTES - AUTHENTICATION
# ============================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student Registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(name=name, email=email, role='student')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User Login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'student')  # student or admin
        
        if not email or not password:
            flash('Email and password required.', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email, role=role).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            
            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        
        flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User Logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ============================================================
# ROUTES - MAIN PAGES
# ============================================================

@app.route('/')
@app.route('/index')
def index():
    """Home Page - Show all approved events"""
    # Get only approved events
    events = Event.query.filter_by(status='success').order_by(Event.date.desc()).all()
    
    return render_template('index.html', events=events)

@app.route('/join-event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    """Join or cancel an event (Student only)"""
    if current_user.is_admin():
        flash('Admins cannot join events', 'danger')
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(event_id)
    action = request.form.get('action', 'join')
    
    try:
        if action == 'join':
            # Check if already registered
            existing = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
            if existing:
                flash('You are already registered for this event.', 'info')
                return redirect(url_for('event_details', event_id=event_id))
            
            registration = Registration(user_id=current_user.id, event_id=event_id, status='registered')
            db.session.add(registration)
            db.session.commit()
            flash('Successfully registered for the event!', 'success')
        
        elif action == 'cancel':
            registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
            if registration:
                db.session.delete(registration)
                db.session.commit()
                flash('Registration cancelled successfully.', 'success')
            else:
                flash('You are not registered for this event.', 'info')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/event/<int:event_id>')
def event_details(event_id):
    """View event details"""
    event = Event.query.get_or_404(event_id)
    
    user_registration = None
    if current_user.is_authenticated and not current_user.is_admin():
        user_registration = Registration.query.filter_by(user_id=current_user.id, event_id=event_id).first()
    
    return render_template('event_details.html', event=event, user_registration=user_registration)

@app.route('/my-events')
@login_required
def my_events():
    """View user's registered events"""
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))
    
    registrations = Registration.query.filter_by(user_id=current_user.id).all()
    
    # Count upcoming and interested events
    from datetime import datetime
    upcoming_events = Event.query.filter(Event.date > datetime.utcnow(), Event.status == 'success').count()
    interested_count = 3  # Placeholder for interested events
    
    return render_template('my_events.html', registrations=registrations, upcoming_count=upcoming_events, interested_count=interested_count)

# ============================================================
# ROUTES - ADMIN DASHBOARD
# ============================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin Dashboard - Overview"""
    total_events = Event.query.count()
    total_users = User.query.filter_by(role='student').count()
    total_registrations = Registration.query.count()
    pending_events = Event.query.filter_by(status='pending').count()
    
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
    
    return render_template('admin/admin_dashboard.html',
                         total_events=total_events,
                         total_users=total_users,
                         total_registrations=total_registrations,
                         pending_events=pending_events,
                         recent_events=recent_events)

@app.route('/admin/create-event', methods=['GET', 'POST'])
@admin_required
def create_event():
    """Create new event"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        date_str = request.form.get('date', '')
        venue = request.form.get('venue', '').strip()
        status = request.form.get('status', 'pending')
        
        if not all([title, description, date_str, venue]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('create_event'))
        
        # Parse date
        try:
            event_date = datetime.fromisoformat(date_str)
        except:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('create_event'))
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_filename = save_upload_file(file)
        
        event = Event(
            title=title,
            description=description,
            date=event_date,
            venue=venue,
            image_filename=image_filename,
            status=status
        )
        
        try:
            db.session.add(event)
            db.session.commit()
            flash(f'Event "{title}" created successfully!', 'success')
            return redirect(url_for('manage_events'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'danger')
    
    return render_template('admin/create_event.html')

@app.route('/admin/manage-events')
@admin_required
def manage_events():
    """Manage events - List all events"""
    events = Event.query.order_by(Event.created_at.desc()).all()
    
    return render_template('admin/manage_events.html', events=events)

@app.route('/admin/event/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    """Edit event"""
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form.get('title', event.title).strip()
        event.description = request.form.get('description', event.description).strip()
        event.venue = request.form.get('venue', event.venue).strip()
        event.status = request.form.get('status', event.status)
        
        # Handle date
        date_str = request.form.get('date', '')
        if date_str:
            try:
                event.date = datetime.fromisoformat(date_str)
            except:
                flash('Invalid date format.', 'danger')
                return redirect(url_for('edit_event', event_id=event_id))
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_filename = save_upload_file(file)
                if image_filename:
                    event.image_filename = image_filename
        
        try:
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('manage_events'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating event: {str(e)}', 'danger')
    
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/event/<int:event_id>/delete', methods=['POST'])
@admin_required
def delete_event(event_id):
    """Delete event"""
    event = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash(f'Event "{event.title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'danger')
    
    return redirect(url_for('manage_events'))

@app.route('/admin/event/<int:event_id>/approve', methods=['GET'])
@admin_required
def approve_event(event_id):
    """Approve event (change status to success)"""
    event = Event.query.get_or_404(event_id)
    event.status = 'success'
    
    try:
        db.session.commit()
        flash(f'Event "{event.title}" approved!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving event: {str(e)}', 'danger')
    
    return redirect(url_for('manage_events'))

@app.route('/admin/registrations')
@admin_required
def manage_registrations():
    """Manage event registrations"""
    registrations = Registration.query.order_by(Registration.registered_at.desc()).all()
    total_registrations = len(registrations)
    registered_count = len([r for r in registrations if r.status == 'registered'])
    pending_count = len([r for r in registrations if r.status == 'pending'])
    
    return render_template('admin/manage_registrations.html', 
                         registrations=registrations,
                         total_registrations=total_registrations,
                         registered_count=registered_count,
                         pending_count=pending_count)

@app.route('/admin/users')
@admin_required
def manage_users():
    """Manage users"""
    users = User.query.order_by(User.created_at.desc()).all()
    total_users = len(users)
    admin_count = len([u for u in users if u.is_admin()])
    student_count = len([u for u in users if not u.is_admin()])
    
    return render_template('admin/manage_users.html', 
                         users=users,
                         total_users=total_users,
                         admin_count=admin_count,
                         student_count=student_count)

@app.route('/admin/add-sample-events')
def add_sample_events():
    """Add sample events to database (Admin only)"""
    try:
        # Check if events already exist
        if Event.query.first():
            flash('Events already exist in database!', 'info')
            return redirect(url_for('manage_events'))
        
        # Create sample events
        sample_events = [
            Event(
                title='Python Workshop 2026',
                description='Learn Python programming from basics to advanced. This workshop covers data structures, OOP, web development with Flask, and best practices. Perfect for beginners and intermediate developers.',
                date=datetime(2026, 4, 15, 10, 0),
                venue='Building A, Room 101',
                image_filename='https://images.unsplash.com/photo-1526374965328-7f5ae4e8290f?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Web Development Bootcamp',
                description='Complete web development bootcamp covering HTML, CSS, JavaScript, and modern frameworks. Build real-world projects and learn industry best practices.',
                date=datetime(2026, 4, 20, 9, 30),
                venue='Tech Hub, Conference Hall',
                image_filename='https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Data Science & Machine Learning',
                description='Introduction to data science, data analysis, and machine learning algorithms. Learn with Python, NumPy, Pandas, and Scikit-learn. Hands-on projects included.',
                date=datetime(2026, 4, 25, 14, 0),
                venue='Innovation Center, Lab 5',
                image_filename='https://images.unsplash.com/photo-1516321318423-f06f70a504f9?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Database Design Mastery',
                description='Master SQL, database design patterns, and optimization. Learn MySQL, PostgreSQL, and NoSQL databases. Practical exercises with real-world scenarios.',
                date=datetime(2026, 5, 1, 10, 0),
                venue='Building B, Room 205',
                image_filename='https://images.unsplash.com/photo-1520004434532-668416a08753?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Cloud Computing with AWS',
                description='Deep dive into AWS cloud services. Learn EC2, S3, Lambda, RDS, and more. Deploy applications to the cloud and scale them efficiently.',
                date=datetime(2026, 5, 5, 15, 30),
                venue='Tech Campus, Room 310',
                image_filename='https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Software Testing & QA',
                description='Comprehensive guide to software testing, unit testing, integration testing, and automation. Learn Selenium, REST API testing, and quality assurance best practices.',
                date=datetime(2026, 5, 10, 11, 0),
                venue='Quality Assurance Lab, Room 150',
                image_filename='https://images.unsplash.com/photo-1525694914303-e49f1d97b1f4?w=500&h=300&fit=crop',
                status='success'
            ),
        ]
        
        for event in sample_events:
            db.session.add(event)
        
        db.session.commit()
        flash('✅ 6 sample events added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding sample events: {str(e)}', 'danger')
    
    return redirect(url_for('manage_events'))

@app.route('/admin/add-hackathon-events')
def add_hackathon_events():
    """Add Hackathon events to database"""
    try:
        # Create hackathon events
        hackathon_events = [
            Event(
                title='Hackathon 2026',
                description='Annual 24-hour coding competition. Build innovative projects, compete with peers, and win exciting prizes. Open to all skill levels. Food and accommodation provided.',
                date=datetime(2026, 5, 13, 10, 0),
                venue='Innovation Hub',
                image_filename='https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=500&h=300&fit=crop',
                status='success'
            ),
            Event(
                title='Hackathon 2026',
                description='Extended hackathon event at our campus auditorium. Network with industry professionals, showcase your skills, and get mentoring from experienced developers.',
                date=datetime(2026, 5, 13, 10, 0),
                venue='Campus Auditorium',
                image_filename='https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=300&fit=crop',
                status='success'
            ),
        ]
        
        for event in hackathon_events:
            # Check if this event already exists
            existing = Event.query.filter_by(title=event.title, venue=event.venue).first()
            if not existing:
                db.session.add(event)
        
        db.session.commit()
        flash('✅ Hackathon events added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding hackathon events: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

@app.route('/admin/update-all-events-images')
def update_all_events_images():
    """Update all events with images"""
    try:
        # Define all events with images
        all_events_data = [
            {
                'title': 'Python Workshop 2026',
                'description': 'Learn Python programming from basics to advanced. This workshop covers data structures, OOP, web development with Flask, and best practices. Perfect for beginners and intermediate developers.',
                'date': datetime(2026, 4, 15, 10, 0),
                'venue': 'Building A, Room 101',
                'image': 'https://images.pexels.com/photos/18069/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Web Development Bootcamp',
                'description': 'Complete web development bootcamp covering HTML, CSS, JavaScript, and modern frameworks. Build real-world projects and learn industry best practices.',
                'date': datetime(2026, 4, 20, 9, 30),
                'venue': 'Tech Hub, Conference Hall',
                'image': 'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Data Science & Machine Learning',
                'description': 'Introduction to data science, data analysis, and machine learning algorithms. Learn with Python, NumPy, Pandas, and Scikit-learn. Hands-on projects included.',
                'date': datetime(2026, 4, 25, 14, 0),
                'venue': 'Innovation Center, Lab 5',
                'image': 'https://images.pexels.com/photos/8386434/pexels-photo-8386434.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Database Design Mastery',
                'description': 'Master SQL, database design patterns, and optimization. Learn MySQL, PostgreSQL, and NoSQL databases. Practical exercises with real-world scenarios.',
                'date': datetime(2026, 5, 1, 10, 0),
                'venue': 'Building B, Room 205',
                'image': 'https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Cloud Computing with AWS',
                'description': 'Deep dive into AWS cloud services. Learn EC2, S3, Lambda, RDS, and more. Deploy applications to the cloud and scale them efficiently.',
                'date': datetime(2026, 5, 5, 15, 30),
                'venue': 'Tech Campus, Room 310',
                'image': 'https://images.pexels.com/photos/7974/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Software Testing & QA',
                'description': 'Comprehensive guide to software testing, unit testing, integration testing, and automation. Learn Selenium, REST API testing, and quality assurance best practices.',
                'date': datetime(2026, 5, 10, 11, 0),
                'venue': 'Quality Assurance Lab, Room 150',
                'image': 'https://images.pexels.com/photos/5632399/pexels-photo-5632399.jpeg?auto=compress&cs=tinysrgb&w=600'
            },
            {
                'title': 'Hackathon 2026',
                'description': 'Annual 24-hour coding competition. Build innovative projects, compete with peers, and win exciting prizes. Open to all skill levels. Food and accommodation provided.',
                'date': datetime(2026, 5, 13, 10, 0),
                'venue': 'Innovation Hub',
                'image': 'https://t3.ftcdn.net/jpg/05/89/74/02/360_F_589740225_TEoGKvUForxAagvPuYwU0TF76j8MUkp3.jpg'
            },
            {
                'title': 'Hackathon 2026',
                'description': 'Extended hackathon event at our campus auditorium. Network with industry professionals, showcase your skills, and get mentoring from experienced developers.',
                'date': datetime(2026, 5, 13, 10, 0),
                'venue': 'Campus Auditorium',
                'image': 'https://t3.ftcdn.net/jpg/05/89/74/02/360_F_589740225_TEoGKvUForxAagvPuYwU0TF76j8MUkp3.jpg'
            },
        ]
        
        # Update or create events
        for event_data in all_events_data:
            existing_event = Event.query.filter_by(title=event_data['title'], venue=event_data['venue']).first()
            if existing_event:
                # Update image if it exists
                existing_event.image_filename = event_data['image']
            else:
                # Create new event
                new_event = Event(
                    title=event_data['title'],
                    description=event_data['description'],
                    date=event_data['date'],
                    venue=event_data['venue'],
                    image_filename=event_data['image'],
                    status='success'
                )
                db.session.add(new_event)
        
        db.session.commit()
        flash('✅ All events updated with images successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating events: {str(e)}', 'danger')
    
    return redirect(url_for('index'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    if user_id == current_user.id:
        flash('Cannot delete your own account!', 'danger')
        return redirect(url_for('manage_users'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('manage_users'))

@app.route('/admin/user/<int:user_id>/promote', methods=['POST'])
@admin_required
def promote_user(user_id):
    """Promote user to admin"""
    if user_id == current_user.id:
        flash('Cannot change your own role!', 'danger')
        return redirect(url_for('manage_users'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        if user.role == 'student':
            user.role = 'admin'
            db.session.commit()
            flash(f'User "{user.name}" promoted to admin!', 'success')
        else:
            flash('User is already an admin.', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error promoting user: {str(e)}', 'danger')
    
    return redirect(url_for('manage_users'))

@app.route('/admin/registration/<int:registration_id>/delete', methods=['POST'])
@admin_required
def delete_registration(registration_id):
    """Delete a registration"""
    registration = Registration.query.get_or_404(registration_id)
    event_id = registration.event_id
    
    try:
        db.session.delete(registration)
        db.session.commit()
        flash('Registration deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting registration: {str(e)}', 'danger')
    
    return redirect(url_for('manage_registrations'))

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    return render_template('errors/403.html'), 403

# ============================================================
# SHELL CONTEXT
# ============================================================

@app.shell_context_processor
def make_shell_context():
    """Make models available in Flask shell"""
    return {'db': db, 'User': User, 'Event': Event, 'Registration': Registration}

# ============================================================
# INITIALIZATION & MAIN
# ============================================================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if data already exists
        if User.query.first():
            return
        
        # Create admin user
        admin = User(name='Admin User', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create student user
        student = User(name='Student User', email='student@example.com', role='student')
        student.set_password('student123')
        db.session.add(student)
        
        db.session.commit()
        
        # Add sample events
        sample_events = [
            Event(
                title='Python Workshop 2026',
                description='Learn Python programming from basics to advanced. This workshop covers data structures, OOP, web development with Flask, and best practices. Perfect for beginners and intermediate developers.',
                date=datetime(2026, 4, 15, 10, 0),
                venue='Building A, Room 101',
                status='success'
            ),
            Event(
                title='Web Development Bootcamp',
                description='Complete web development bootcamp covering HTML, CSS, JavaScript, and modern frameworks. Build real-world projects and learn industry best practices.',
                date=datetime(2026, 4, 20, 9, 30),
                venue='Tech Hub, Conference Hall',
                status='success'
            ),
            Event(
                title='Data Science & Machine Learning',
                description='Introduction to data science, data analysis, and machine learning algorithms. Learn with Python, NumPy, Pandas, and Scikit-learn. Hands-on projects included.',
                date=datetime(2026, 4, 25, 14, 0),
                venue='Innovation Center, Lab 5',
                status='success'
            ),
            Event(
                title='Database Design Mastery',
                description='Master SQL, database design patterns, and optimization. Learn MySQL, PostgreSQL, and NoSQL databases. Practical exercises with real-world scenarios.',
                date=datetime(2026, 5, 1, 10, 0),
                venue='Building B, Room 205',
                status='success'
            ),
            Event(
                title='Cloud Computing with AWS',
                description='Deep dive into AWS cloud services. Learn EC2, S3, Lambda, RDS, and more. Deploy applications to the cloud and scale them efficiently.',
                date=datetime(2026, 5, 5, 15, 30),
                venue='Tech Campus, Room 310',
                status='success'
            ),
            Event(
                title='Software Testing & QA',
                description='Comprehensive guide to software testing, unit testing, integration testing, and automation. Learn Selenium, REST API testing, and quality assurance best practices.',
                date=datetime(2026, 5, 10, 11, 0),
                venue='Quality Assurance Lab, Room 150',
                status='success'
            ),
        ]
        
        for event in sample_events:
            db.session.add(event)
        
        db.session.commit()
        
        print("✅ Database initialized with default users and sample events!")
        print("Admin: admin@example.com / admin123")
        print("Student: student@example.com / student123")
        print("📅 6 sample events added to the database")

if __name__ == '__main__':
    init_db()
    print("\n🚀 Starting Event Management System...")
    print("📝 Access the application at: http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)