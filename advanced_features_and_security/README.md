# Introduction to Django Project

## Setup Instructions
1. Install Django:
```bash
pip install django
```

2. Create the project:
```bash
django-admin startproject LibraryProject
cd LibraryProject
python manage.py startapp bookshelf
```

3. Add 'bookshelf' to INSTALLED_APPS in settings.py

4. Create and apply migrations:
```bash
python manage.py makemigrations bookshelf
python manage.py migrate
```

5. Create superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
- LibraryProject/ - Main project directory
- bookshelf/ - App containing Book model
- create.md - Create operation documentation
- retrieve.md - Retrieve operation documentation
- update.md - Update operation documentation
- delete.md - Delete operation documentation
