# LibraryProject

This is a Django project for managing a library system with books, authors, libraries, and user roles.

## Features

- Custom User Model with additional fields (date_of_birth, profile_photo)
- Book management with permissions
- User roles: Admin, Librarian, Member
- Security headers implemented (X-Frame-Options, Content-Security-Policy, etc.)

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

4. Run the server:
   ```
   python manage.py runserver
   ```

## Security

The project implements the following security headers:
- X-Frame-Options: DENY
- Content-Security-Policy: Configured via django-csp
- Strict-Transport-Security: Configured for HTTPS
- X-Content-Type-Options: nosniff
- Referrer-Policy: same-origin
- Cross-Origin-Opener-Policy: same-origin

## Permissions

Custom permissions defined for Book model:
- can_view: Can view books
- can_create: Can create books
- can_edit: Can edit books
- can_delete: Can delete books
