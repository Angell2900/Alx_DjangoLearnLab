# Library Project

A Django-based library management system built as part of the Introduction to Django course.

## Project Structure
- `bookshelf/` - Main application for book management
- `LibraryProject/` - Project configuration directory
- `manage.py` - Django's command-line utility

## Setup Instructions
1. Install dependencies:
```bash
pip install django
```

2. Initialize database:
```bash
python manage.py migrate
```

3. Create admin user:
```bash
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

## Features
- Book management system
- Admin interface for data management
- CRUD operations for books
