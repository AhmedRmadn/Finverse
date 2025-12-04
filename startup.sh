#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Finverse setup..."

# 0. Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 No .env found. Creating one from .env.example..."
    cp .env.example .env
else
    echo "✅ .env already exists. Skipping copy."
fi

# 1. Build and Start Containers
echo "🐳 Building and starting Docker containers..."
docker compose up -d --build

# 2. Wait for the Web Container
# Even though we use depends_on, we give it a moment to ensure the Python process is listening
echo "⏳ Waiting for Django to be ready..."
sleep 5

# 3. Apply Database Migrations
echo "📦 Applying database migrations..."
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# 4. Create Superuser (Idempotent)
# This Python script checks if the user exists first to avoid errors on repeated runs.
echo "👤 Creating superuser (if not exists)..."
docker compose exec web python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@finverse.com')
PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print(f'✅ Superuser \"{USERNAME}\" created successfully!')
else:
    print(f'⚠️ Superuser \"{USERNAME}\" already exists. Skipping creation.')
"

# 5. Collect Static Files (Optional but good for CSS)
echo "🎨 Collecting static files..."
docker compose exec web python manage.py collectstatic --noinput

echo "=========================================="
echo "✅ Setup Complete!"
echo "🌍 Server running at: http://localhost:8000"
echo "🔐 Admin credentials: admin / admin123" 
echo "=========================================="