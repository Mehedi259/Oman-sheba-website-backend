#!/bin/bash

# Sheba Backend Setup Script

echo "🚀 Setting up Sheba Backend..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if needed
echo ""
echo "✅ Setup complete!"
echo ""
echo "To create admin user, run:"
echo "  python manage.py createsuperuser"
echo ""
echo "To start the server, run:"
echo "  python manage.py runserver"
echo ""
