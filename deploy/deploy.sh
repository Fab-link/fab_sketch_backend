#!/bin/bash

# FabSketch Backend Deployment Script for EC2
# Usage: ./deploy.sh [EC2_IP]

set -e

# Configuration
EC2_IP=${1:-"10.0.10.18"}
KEY_PATH="~/.ssh/fabsketch-key"
PROJECT_NAME="fabsketch_backend"
DEPLOY_PATH="/opt/fabsketch"

echo "🚀 Starting deployment to EC2: $EC2_IP"

# 1. Create deployment package
echo "📦 Creating deployment package..."
cd "$(dirname "$0")/.."
tar --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' \
    -czf "${PROJECT_NAME}.tar.gz" .

# 2. Upload to EC2
echo "📤 Uploading to EC2..."
scp -i $KEY_PATH "${PROJECT_NAME}.tar.gz" ec2-user@$EC2_IP:/tmp/

# 3. Deploy on EC2
echo "🔧 Deploying on EC2..."
ssh -i $KEY_PATH ec2-user@$EC2_IP << 'EOF'
set -e

# Stop existing service
sudo pkill -f gunicorn || true

# Backup current deployment
if [ -d "/opt/fabsketch" ]; then
    sudo mv /opt/fabsketch /opt/fabsketch_backup_$(date +%Y%m%d_%H%M%S)
fi

# Create deployment directory
sudo mkdir -p /opt/fabsketch
cd /opt/fabsketch

# Extract new code
sudo tar -xzf /tmp/fabsketch_backend.tar.gz
sudo chown -R ec2-user:ec2-user /opt/fabsketch

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Use EC2 settings
export DJANGO_SETTINGS_MODULE=deploy.ec2_settings

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn --bind 0.0.0.0:8000 \
         --workers 2 \
         --timeout 120 \
         --daemon \
         --pid /opt/fabsketch/gunicorn.pid \
         --access-logfile /opt/fabsketch/access.log \
         --error-logfile /opt/fabsketch/error.log \
         --env DJANGO_SETTINGS_MODULE=deploy.ec2_settings \
         fab_sketch_project.wsgi:application

echo "✅ Deployment completed successfully!"
EOF

# 4. Cleanup
rm "${PROJECT_NAME}.tar.gz"

# 5. Health check
echo "🔍 Running health check..."
sleep 5
curl -f http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/ || {
    echo "❌ Health check failed!"
    exit 1
}

echo "🎉 Deployment successful! Backend is running at:"
echo "   Health: http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/health/"
echo "   Admin:  http://fab-sketch-alb-1270525117.ap-northeast-2.elb.amazonaws.com/admin/"
