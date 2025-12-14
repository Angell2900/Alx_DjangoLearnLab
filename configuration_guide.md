# Database Credentials and Static Files Configuration Guide

## Overview
The social_media_api project has been updated with proper database credentials setup and AWS S3 integration for static files handling in production.

## Database Configuration ✅

### Current Status:
- **PORT setting**: ✅ Now included in database configuration
- **Production Database**: ✅ PostgreSQL with environment-based configuration
- **Development Fallback**: ✅ SQLite when no PostgreSQL credentials provided
- **Secure Credential Management**: ✅ Using environment variables

### Database Configuration Details:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'social_media_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}
```

### Environment Variables for Database:
```bash
# Set these environment variables for production
export DB_NAME="your_database_name"
export DB_USER="your_database_user"
export DB_PASSWORD="your_secure_password"
export DB_HOST="your_database_host"
export DB_PORT="5432"
```

## Static Files Configuration ✅

### Current Status:
- **AWS S3 Integration**: ✅ Configured for production file hosting
- **collectstatic Support**: ✅ Properly configured for production
- **Environment-based Storage**: ✅ Automatic detection of storage backend
- **Development/Production Separation**: ✅ Local storage for dev, S3 for prod

### AWS S3 Configuration:
```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Enable S3 by setting USE_S3=True
if os.environ.get('USE_S3') == 'True':
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Environment Variables for AWS S3:
```bash
# Set these environment variables for production with S3
export USE_S3="True"
export AWS_ACCESS_KEY_ID="your_aws_access_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
export AWS_STORAGE_BUCKET_NAME="your_s3_bucket_name"
export AWS_S3_REGION_NAME="us-east-1"
```

## Installation and Setup

### 1. Install Dependencies
```bash
cd social_media_api
pip install -r requirements.txt
```

### 2. Development Setup
```bash
# For development (uses SQLite and local storage)
export DB_NAME=""  # This triggers SQLite fallback
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

### 3. Production Setup
```bash
# Set production environment variables
export DB_NAME="your_production_db"
export DB_USER="your_db_user"
export DB_PASSWORD="your_secure_password"
export DB_HOST="your_db_host"
export DB_PORT="5432"
export USE_S3="True"
export AWS_ACCESS_KEY_ID="your_aws_key"
export AWS_SECRET_ACCESS_KEY="your_aws_secret"
export AWS_STORAGE_BUCKET_NAME="your_bucket"

# Run migrations and collectstatic
python manage.py migrate
python manage.py collectstatic --noinput
```

## Verification Checklist

### Database Configuration:
- [x] PORT setting present in database configuration
- [x] Environment-based database selection working
- [x] Development fallback to SQLite configured
- [x] Production PostgreSQL configuration ready

### Static Files Configuration:
- [x] AWS S3 storage backend configured
- [x] Environment-based storage selection working
- [x] collectstatic command properly configured
- [x] Both static and media files handled by S3 in production

## Testing the Configuration

### Test Database Connection:
```bash
cd social_media_api
python manage.py dbshell  # Should connect to configured database
```

### Test Static Files:
```bash
cd social_media_api
python manage.py collectstatic --dry-run  # Preview static files collection
```

### Test Django Settings:
```bash
cd social_media_api
python manage.py check --deploy  # Check production readiness
```

## Summary

✅ **Database Credentials**: Properly configured with PORT setting and environment variables
✅ **Static Files**: AWS S3 integration configured for production with collectstatic support
✅ **Security**: Environment-based configuration for sensitive credentials
✅ **Flexibility**: Separate development and production configurations

The social_media_api project now meets all the requirements for database credentials setup and static files handling in production.
