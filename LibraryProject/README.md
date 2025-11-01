# Library Project

A Django-based library management system that helps track books and manage library operations.

## Features
- Book management (add, edit, delete books)
- Book details tracking (title, author, ISBN, etc.)
- Simple book search and filtering

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: 
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## Project Structure
- `bookshelf/` - Main app for book management
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)

## Technologies
- Django
- SQLite (default database)
- Bootstrap (for styling)
