# ⚡ Quick Start - Deploy Sheba Backend

Follow these steps to deploy your backend to Hetzner server with CI/CD.

## 📋 Prerequisites Checklist

✅ GitHub repository pushed: https://github.com/Mehedi259/Oman-sheba-website-backend.git  
✅ Server created: 188.245.212.240  
✅ SSH key generated: `~/.ssh/sheba_hetzner`  
✅ SSH key added to server  

## 🎯 Step 1: Configure GitHub Secrets (5 minutes)

### Go to GitHub Repository Settings
1. Open: https://github.com/Mehedi259/Oman-sheba-website-backend/settings/secrets/actions
2. Click **"New repository secret"**

### Add 3 Secrets:

#### Secret 1: SERVER_HOST
```
Name: SERVER_HOST
Value: 188.245.212.240
```

#### Secret 2: SERVER_USER
```
Name: SERVER_USER
Value: root
```

#### Secret 3: SSH_PRIVATE_KEY
```
Name: SSH_PRIVATE_KEY
Value: [Copy entire SSH private key - see below]
```

**To get SSH private key:**
```bash
cat ~/.ssh/sheba_hetzner
```

Copy everything from:
```
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

## 🚀 Step 2: Initial Server Setup (10 minutes)

### Connect to Server
```bash
ssh -i ~/.ssh/sheba_hetzner root@188.245.212.240
```

### Clone Repository
```bash
cd /var/www
git clone https://github.com/Mehedi259/Oman-sheba-website-backend.git sheba
cd sheba
```

### Run Setup Script
```bash
chmod +x deploy_scripts/setup_server.sh
bash deploy_scripts/setup_server.sh
```

**This will take ~5 minutes and will:**
- Install all dependencies
- Setup PostgreSQL database
- Configure Nginx + Gunicorn
- Run migrations
- Create admin user

### Configure Environment
```bash
nano /var/www/sheba/.env
```

**Update these lines:**
```env
SECRET_KEY=<generate-new-key>
DEBUG=False
ALLOWED_HOSTS=188.245.212.240
CORS_ALLOWED_ORIGINS=http://188.245.212.240,https://yourdomain.com
```

**Generate SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Restart Services
```bash
sudo systemctl restart gunicorn
sudo systemctl reload nginx
```

## ✅ Step 3: Test Deployment

### Check if Backend is Running
Open in browser: http://188.245.212.240

### Access Admin Panel
URL: http://188.245.212.240/admin  
Username: `admin`  
Password: `admin123`

**⚠️ Change password immediately!**

### Check API Documentation
- Swagger: http://188.245.212.240/swagger
- Redoc: http://188.245.212.240/redoc

## 🔄 Step 4: Test CI/CD (2 minutes)

### Make a Test Change
```bash
# On your local machine
cd /Users/mehedihasanmridul/Backend/ShebaWebsiteBackend

# Edit README
echo "Updated: $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI/CD deployment"
git push origin main
```

### Watch GitHub Actions
1. Go to: https://github.com/Mehedi259/Oman-sheba-website-backend/actions
2. Watch the deployment workflow run
3. Should complete in ~1-2 minutes

### Verify on Server
```bash
ssh -i ~/.ssh/sheba_hetzner root@188.245.212.240
cd /var/www/sheba
git log -1  # Should show your latest commit
```

## 🎉 Done!

Your backend is now deployed with automatic CI/CD!

**Every time you push to `main` branch:**
1. GitHub Actions triggers automatically
2. Code is deployed to server
3. Dependencies are updated
4. Migrations run
5. Static files collected
6. Gunicorn restarts
7. Done! ✅

## 🔍 Useful Commands

### Check Service Status
```bash
# On server
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### View Logs
```bash
# Application logs
tail -f /var/log/gunicorn/sheba_access.log
tail -f /var/log/gunicorn/sheba_error.log

# Gunicorn service logs
sudo journalctl -u gunicorn -f
```

### Manual Deployment
```bash
# If GitHub Actions fails, deploy manually
cd /var/www/sheba
bash deploy_scripts/update_deploy.sh
```

## ⚠️ Important Security Notes

1. ✅ Change admin password immediately
2. ✅ Generate new SECRET_KEY for production
3. ✅ Set DEBUG=False
4. ✅ Configure proper ALLOWED_HOSTS
5. ⏳ Setup SSL certificate (recommended)
6. ⏳ Configure firewall
7. ⏳ Setup database backups

## 📞 Need Help?

- **Full Guide**: See `DEPLOYMENT.md` for detailed documentation
- **Server Issues**: Check logs with commands above
- **GitHub Actions**: View workflow logs in Actions tab
- **Database**: Connect with `sudo -u postgres psql sheba_db`

## 📊 Current Setup

| Component | Status | Details |
|-----------|--------|---------|
| Server | ✅ Ready | 188.245.212.240 |
| Database | ✅ Created | PostgreSQL (sheba_db) |
| Web Server | ✅ Configured | Nginx + Gunicorn |
| SSH Access | ✅ Working | Key-based auth |
| GitHub Repo | ✅ Pushed | Latest code |
| CI/CD | ⏳ Setup | Add secrets to enable |

---

**Next**: Configure GitHub Secrets (Step 1) to enable automatic deployments!
