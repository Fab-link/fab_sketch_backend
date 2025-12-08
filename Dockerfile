FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setup database and create test data
RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@test.com', 'admin123', nickname='Admin') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]
