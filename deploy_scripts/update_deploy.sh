#!/bin/bash

# Sheba Backend - Update & Deploy Script
# This script is run by GitHub Actions on every push

set -e

echo "🔄 Updating Sheba Backend..."

PROJECT_DIR="/var/www/sheba"
VENV_DIR="$PROJECT_DIR/venv"

cd $PROJECT_DIR

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install/Update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

# Set proper permissions
echo "🔧 Setting permissions..."
sudo chown -R www-data:www-data $PROJECT_DIR/media
sudo chown -R www-data:www-data $PROJECT_DIR/staticfiles

# Restart Gunicorn
echo "🔄 Restarting Gunicorn..."
sudo systemctl restart gunicorn

# Reload Nginx
echo "🌐 Reloading Nginx..."
sudo systemctl reload nginx

echo "✅ Deployment completed successfully!"
