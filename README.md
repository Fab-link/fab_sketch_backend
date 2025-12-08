# FabSketch Backend

Django REST API for FabSketch 0.1.0

## 🌐 Live Deployment

**Production URL**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com

### API Endpoints
- **API Root**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/
- **Health Check**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/
- **Designs**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/designs/
- **Comments**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/comments/
- **Users**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/users/

## 🚀 Local Development

### Prerequisites
- **Python 3.11+**: [Download here](https://www.python.org/downloads/)
- **Git**: For cloning the repository

### Initial Setup (First Time)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FabSketch/fab_sketch_backend
   ```

2. **Create Python Virtual Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate it
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate     # Windows
   
   # Verify activation (should show venv path)
   which python
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Setup Database**
   ```bash
   # Create SQLite database and tables
   python manage.py migrate
   
   # Create admin user (follow prompts)
   python manage.py createsuperuser
   
   # Create test data (optional but recommended)
   python manage.py create_test_data
   ```

5. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

### Daily Development

```bash
# 1. Activate Python environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. Start Django server
python manage.py runserver
```

### Local Access Points
- **API Root**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

### Stopping Services
```bash
# Stop Django server: Ctrl+C
# Deactivate Python environment
deactivate
```

## 🗄️ Database Information

**Local Development**: SQLite database (`db.sqlite3`)
**Production**: SQLite in ECS container (ephemeral storage)

⚠️ **Note**: Production data is not persistent across container restarts

## 🔧 Troubleshooting

### Common Issues

**1. Docker not running**
```
Error: Cannot connect to Docker daemon
```
**Solution**: Start Docker Desktop application

**2. Port 5432 already in use**
```
Error: port is already allocated
```
**Solution**: Stop local PostgreSQL or change port in docker-compose.yml

**3. Python virtual environment issues**
```bash
# Remove and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Database connection errors**
```bash
# Check if database container is running
docker-compose ps

# Restart database
docker-compose restart db
```

### Environment Variables

Create `.env` file if needed (already exists):
```env
DEBUG=True
SECRET_KEY=django-insecure-demo-key-change-in-production
DB_NAME=fab_sketch_db
DB_USER=fab_sketch_user
DB_PASSWORD=fab_sketch_pass
DB_HOST=localhost
DB_PORT=5432
```

## 📋 Development Commands

```bash
# Create new Django app
python manage.py startapp app_name

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

## 🏗️ Project Structure

```
fab_sketch_backend/
├── fab_sketch_project/     # Django project settings
├── users/                  # User management app
├── designs/               # Design management app
├── comments/              # Comment system app
├── social/                # Like/Bookmark/Follow app
├── venv/                  # Python virtual environment
├── docker-compose.yml     # Database container
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── manage.py             # Django management script
```

## 🤝 Team Development

### Before Starting Work
```bash
git pull origin main
docker-compose up -d
source venv/bin/activate
python manage.py migrate  # Apply any new migrations
```

### After Making Changes
```bash
# If you modified models
python manage.py makemigrations
python manage.py migrate

# Commit your changes
git add .
git commit -m "Your commit message"
git push origin your-branch
```

## 📞 Need Help?

1. Check this README first
2. Look at Django/Docker documentation
3. Ask team members
4. Create an issue in the repository
