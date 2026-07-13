#!/bin/bash

# Sheba Backend - Initial Server Setup Script
# Run this script once on the server after cloning the repository

set -e  # Exit on error

echo "🚀 Starting Sheba Backend Server Setup..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/sheba"
VENV_DIR="$PROJECT_DIR/venv"
GUNICORN_SOCKET="/run/gunicorn.sock"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Installing system dependencies...${NC}"
apt-get update
apt-get install -y \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    supervisor \
    git \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev

echo -e "${BLUE}🗄️  Configuring PostgreSQL...${NC}"
sudo -u postgres psql -c "CREATE DATABASE sheba_db;" 2>/dev/null || echo "Database already exists"
sudo -u postgres psql -c "CREATE USER sheba_user WITH PASSWORD 'Sheba@2024#Secure';" 2>/dev/null || echo "User already exists"
sudo -u postgres psql -c "ALTER ROLE sheba_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE sheba_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE sheba_user SET timezone TO 'Asia/Muscat';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sheba_db TO sheba_user;"

echo -e "${BLUE}🐍 Setting up Python virtual environment...${NC}"
cd $PROJECT_DIR
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${BLUE}⚙️  Setting up environment variables...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env.production $PROJECT_DIR/.env
    echo -e "${GREEN}✅ Created .env file from template${NC}"
    echo -e "${RED}⚠️  IMPORTANT: Edit /var/www/sheba/.env and update SECRET_KEY and other settings!${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo -e "${BLUE}🗂️  Creating necessary directories...${NC}"
mkdir -p /var/log/gunicorn
mkdir -p /var/run/gunicorn
chown -R www-data:www-data /var/log/gunicorn
chown -R www-data:www-data /var/run/gunicorn

echo -e "${BLUE}📁 Setting up media and static directories...${NC}"
mkdir -p $PROJECT_DIR/media
mkdir -p $PROJECT_DIR/staticfiles
chown -R www-data:www-data $PROJECT_DIR/media
chown -R www-data:www-data $PROJECT_DIR/staticfiles

echo -e "${BLUE}🔄 Running Django migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${BLUE}📊 Collecting static files...${NC}"
python manage.py collectstatic --noinput

echo -e "${BLUE}👤 Creating Django superuser...${NC}"
echo "from users.models import User; User.objects.create_superuser('admin', 'admin@sheba.om', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo -e "${BLUE}⚙️  Setting up Gunicorn service...${NC}"
cat > /etc/systemd/system/gunicorn.service << 'EOF'
[Unit]
Description=Gunicorn daemon for Sheba Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sheba
Environment="PATH=/var/www/sheba/venv/bin"
ExecStart=/var/www/sheba/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    --timeout 120 \
    --access-logfile /var/log/gunicorn/sheba_access.log \
    --error-logfile /var/log/gunicorn/sheba_error.log \
    sheba_backend.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

echo -e "${BLUE}🌐 Setting up Nginx...${NC}"
cat > /etc/nginx/sites-available/sheba << 'EOF'
server {
    listen 80;
    server_name 188.245.212.240;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/sheba/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/sheba/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/sheba /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

echo -e "${BLUE}🔧 Setting permissions...${NC}"
chown -R www-data:www-data $PROJECT_DIR

echo -e "${BLUE}🚀 Starting services...${NC}"
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
systemctl enable nginx
systemctl restart nginx

echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Edit /var/www/sheba/.env and update SECRET_KEY"
echo "2. Update ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS in .env"
echo "3. Access your site at http://188.245.212.240"
echo "4. Admin panel: http://188.245.212.240/admin"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo -e "${BLUE}🔍 Useful commands:${NC}"
echo "  sudo systemctl status gunicorn     # Check Gunicorn status"
echo "  sudo systemctl restart gunicorn    # Restart Gunicorn"
echo "  sudo systemctl status nginx        # Check Nginx status"
echo "  sudo journalctl -u gunicorn -f     # View Gunicorn logs"
echo "  tail -f /var/log/gunicorn/*.log    # View application logs"
