# FabSketch Backend

Django REST API backend for FabSketch mobile application.

## 🏗️ Architecture

```
Flutter App → ALB → EC2 (Django) → RDS PostgreSQL
                 ↘ Lambda (AI Image Generation)
```

## 🚀 Deployment

### Current Infrastructure

- **EC2 Instance**: `i-0241eb14f5097a359` (Private IP: 10.0.10.18)
- **Load Balancer**: `fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com`
- **Database**: `fab-sketch-db.chyooau22dfx.ap-northeast-2.rds.amazonaws.com`
- **Storage**: S3 bucket `fab-sketch-media-xp8zu198`

### Code Changes → Deployment Workflow

**📋 For detailed deployment instructions, see [../DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)**

**After making backend code changes:**

```bash
# 1. Commit your changes
git add .
git commit -m "Fix: your change description"
git push origin main

# 2. Deploy to production (one command!)
cd fab_sketch_backend
./deploy/deploy.sh

# 3. Verify deployment
curl http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/
# Expected: {"status": "healthy"}
```

### Quick Deploy

```bash
# Deploy latest code to EC2
cd fab_sketch_backend
./deploy/deploy.sh

# Or specify EC2 IP
./deploy/deploy.sh 10.0.10.18
```

### Manual Deployment Steps

1. **Prepare deployment package**
   ```bash
   cd fab_sketch_backend
   tar --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' \
       -czf fabsketch_backend.tar.gz .
   ```

2. **Upload to EC2**
   ```bash
   scp -i ~/.ssh/fabsketch-key fabsketch_backend.tar.gz ec2-user@10.0.10.18:/tmp/
   ```

3. **Deploy on EC2**
   ```bash
   ssh -i ~/.ssh/fabsketch-key ec2-user@10.0.10.18
   
   # Stop existing service
   sudo pkill -f gunicorn
   
   # Extract new code
   sudo rm -rf /opt/fabsketch/*
   cd /opt/fabsketch
   sudo tar -xzf /tmp/fabsketch_backend.tar.gz
   sudo chown -R ec2-user:ec2-user /opt/fabsketch
   
   # Setup environment
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Run migrations
   export DJANGO_SETTINGS_MODULE=deploy.ec2_settings
   python manage.py migrate
   python manage.py collectstatic --noinput
   
   # Start service
   gunicorn --bind 0.0.0.0:8000 \
            --workers 2 \
            --daemon \
            --env DJANGO_SETTINGS_MODULE=deploy.ec2_settings \
            fab_sketch_project.wsgi:application
   ```

4. **Verify deployment**
   ```bash
   curl http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/
   ```

## 🔧 Development

### Local Setup

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd fab_sketch_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Environment Variables

Create `.env` file for local development:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=fabsketch_local
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## 📱 API Endpoints

### Base URL
- **Production**: `http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/`
- **Local**: `http://localhost:8000/api/`

### Health Check
- `GET /health/` - Service health status

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout

### Users
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/` - Update user profile

### Designs
- `GET /api/designs/` - List designs (feed)
- `POST /api/designs/` - Create new design
- `GET /api/designs/{id}/` - Get design details

### Comments
- `GET /api/comments/?design_id={id}` - Get design comments
- `POST /api/comments/` - Create comment
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

### Social
- `POST /api/social/like/` - Toggle like
- `POST /api/social/bookmark/` - Toggle bookmark
- `POST /api/social/follow/` - Toggle follow

## 🔍 Monitoring & Logs

### Check service status
```bash
ssh -i ~/.ssh/fabsketch-key ec2-user@10.0.10.18
ps aux | grep gunicorn
```

### View logs
```bash
# Application logs
tail -f /opt/fabsketch/error.log
tail -f /opt/fabsketch/access.log

# System logs
sudo journalctl -u fabsketch -f
```

### Health check
```bash
curl http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/
```

## 🛠️ Troubleshooting

### Service not responding
```bash
# Restart Gunicorn
ssh -i ~/.ssh/fabsketch-key ec2-user@10.0.10.18
sudo pkill -f gunicorn
cd /opt/fabsketch
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 --daemon fab_sketch_project.wsgi:application
```

### Database connection issues
```bash
# Test database connection
python manage.py dbshell
```

### Static files not loading
```bash
# Recollect static files
python manage.py collectstatic --noinput
```

## 📋 Deployment Checklist

Before deploying to production:

- [ ] Update `requirements.txt` with new dependencies
- [ ] Run tests locally: `python manage.py test`
- [ ] Check migrations: `python manage.py makemigrations --dry-run`
- [ ] Update environment variables if needed
- [ ] Test API endpoints locally
- [ ] Backup database if schema changes
- [ ] Deploy using `./deploy/deploy.sh`
- [ ] Verify health check passes
- [ ] Test critical user flows

## 🔐 Security Notes

- EC2 instance is in private subnet (no direct internet access)
- Access only through ALB
- Database credentials stored in environment variables
- Static files served through Django (consider CDN for production)
- CORS enabled for all origins (restrict in production)

## 📞 Support

For deployment issues or questions:
1. Check logs first: `/opt/fabsketch/error.log`
2. Verify health endpoint: `/health/`
3. Check EC2 instance status in AWS Console
4. Review ALB target group health
