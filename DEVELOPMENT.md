# Development Setup Guide

## Quick Setup for Team Members

### 1. Clone and Setup
```bash
git clone https://github.com/Fab-link/fab_sketch_backend.git
cd fab_sketch_backend
cp .env.example .env
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# SQLite (default for development)
python manage.py migrate
python manage.py createsuperuser

# Create test data
python manage.py shell
>>> from users.management.commands.create_test_data import Command
>>> Command().handle()
```

### 4. Run Server
```bash
python manage.py runserver
# API available at: http://localhost:8000/api/
```

## Docker Development (Alternative)
```bash
docker-compose up --build
# API available at: http://localhost:8000/api/
```

## Current Deployment
- **Production URL**: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/api/
- **Admin**: Create superuser locally for development

## API Testing
```bash
# Test registration
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "nickname": "Test User", "password": "test123!"}'

# Test login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123!"}'
```

## Database Schema
- Users: Custom user model with nickname, profile_image, bio
- Designs: title, description, images (sketch, flat, wearing), hashtags
- Comments: content, user, design relationships
- Social: Like, Bookmark, Follow models

## Key Files for Development
- `fab_sketch_project/settings.py` - Django settings
- `fab_sketch_project/urls.py` - URL routing
- `users/auth_views.py` - Authentication endpoints
- `designs/views.py` - Design CRUD operations
- `social/views.py` - Like/bookmark/follow features
