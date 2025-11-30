#!/bin/bash

# Start Django development server

cd /Users/angelibzw/Alx_DjangoLearnLab/advanced-api-project

echo "Starting Django development server..."
echo "=================================="

# Activate virtual environment
source .venv/bin/activate

# Run migrations if needed
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
