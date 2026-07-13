# 🚀 Sheba Backend Deployment Guide

Complete deployment guide for Sheba Backend on Hetzner server with CI/CD.

## 📋 Server Information

- **Server IP**: 188.245.212.240
- **Server Name**: HelloOmanSheba
- **OS**: Ubuntu
- **User**: root
- **Database**: PostgreSQL (sheba_db)
- **Web Server**: Nginx + Gunicorn
- **Python**: 3.14

## 🔐 SSH Access

### SSH Key Location
```bash
~/.ssh/sheba_hetzner
```

### Connect to Server
```bash
ssh -i ~/.ssh/sheba_hetzner root@188.245.212.240
```

## 📦 Initial Server Setup

### 1. Clone Repository on Server
```bash
ssh -i ~/.ssh/sheba_hetzner root@188.245.212.240

# Create project directory
mkdir -p /var/www
cd /var/www

# Clone repository
git clone https://github.com/Mehedi259/Oman-sheba-website-backend.git sheba
cd sheba
```

### 2. Run Initial Setup Script
```bash
chmod +x deploy_scripts/setup_server.sh
bash deploy_scripts/setup_server.sh
```

This script will:
- ✅ Install system dependencies (Python, PostgreSQL, Nginx, etc.)
- ✅ Create PostgreSQL database and user
- ✅ Set up Python virtual environment
- ✅ Install Python dependencies
- ✅ Create .env file from template
- ✅ Run migrations
- ✅ Collect static files
- ✅ Create Django superuser (admin/admin123)
- ✅ Configure Gunicorn service
- ✅ Configure Nginx
- ✅ Start all services

### 3. Configure Environment Variables
```bash
nano /var/www/sheba/.env
```

**Update these settings:**
```env
SECRET_KEY=your-strong-secret-key-here
DEBUG=False
ALLOWED_HOSTS=188.245.212.240,yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

**Generate a secret key:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Restart Services
```bash
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

## 🔄 GitHub Actions CI/CD Setup

### Required GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `SERVER_HOST` | `188.245.212.240` |
| `SERVER_USER` | `root` |
| `SSH_PRIVATE_KEY` | Contents of `~/.ssh/sheba_hetzner` (private key) |

### Get SSH Private Key Content
```bash
cat ~/.ssh/sheba_hetzner
```

Copy the entire output including:
```
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

### How CI/CD Works

1. **Push to main branch** → GitHub Actions triggers automatically
2. **GitHub Actions**:
   - Connects to server via SSH
   - Pulls latest code
   - Runs `deploy_scripts/update_deploy.sh`
   - Updates dependencies
   - Runs migrations
   - Collects static files
   - Restarts Gunicorn
   - Reloads Nginx

## 🔍 Useful Commands

### Service Management
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# Restart Gunicorn
sudo systemctl restart gunicorn

# Check Nginx status
sudo systemctl status nginx

# Restart Nginx
sudo systemctl restart nginx
```

### Logs
```bash
# View Gunicorn logs (live)
sudo journalctl -u gunicorn -f

# View application logs
tail -f /var/log/gunicorn/sheba_access.log
tail -f /var/log/gunicorn/sheba_error.log

# View Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Django Management
```bash
# Activate virtual environment
cd /var/www/sheba
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

### Database Management
```bash
# Access PostgreSQL
sudo -u postgres psql

# Connect to database
\c sheba_db

# List tables
\dt

# Exit
\q
```

## 🌐 Access URLs

- **Frontend API**: http://188.245.212.240
- **Admin Panel**: http://188.245.212.240/admin
- **API Documentation**: http://188.245.212.240/swagger
- **Redoc**: http://188.245.212.240/redoc

### Default Admin Credentials
- **Username**: admin
- **Password**: admin123

**⚠️ Change these immediately in production!**

## 🔒 Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in .env
- [ ] Set DEBUG=False in production
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure firewall (ufw)
- [ ] Regular database backups
- [ ] Keep system and packages updated

## 🔐 SSL Setup (Optional but Recommended)

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

### Get SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com
```

### Auto-renewal
```bash
sudo certbot renew --dry-run
```

## 🐛 Troubleshooting

### Gunicorn won't start
```bash
# Check logs
sudo journalctl -u gunicorn -n 50

# Check socket file
ls -la /run/gunicorn.sock

# Verify permissions
sudo chown -R www-data:www-data /var/www/sheba
```

### Nginx 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn

# Check Nginx error log
tail -f /var/log/nginx/error.log
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "SELECT version();"

# Verify database exists
sudo -u postgres psql -l | grep sheba_db
```

### Static Files Not Loading
```bash
# Recollect static files
cd /var/www/sheba
source venv/bin/activate
python manage.py collectstatic --noinput

# Check permissions
sudo chown -R www-data:www-data /var/www/sheba/staticfiles
```

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Check application logs
- Review Nginx/Gunicorn logs

## 📝 Notes

- Database credentials are stored in `/var/www/sheba/.env`
- Never commit `.env` file to Git
- Backup database regularly
- Monitor disk space and logs
- Keep dependencies updated

---

**Last Updated**: 2026-07-14
