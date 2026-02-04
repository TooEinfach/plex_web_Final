# Deployment Guide

## Production Deployment Options

### Option 1: Traditional Linux Server (Ubuntu/Debian)

#### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Python 3.8+
- PostgreSQL (recommended) or MySQL
- Nginx
- Supervisor or systemd

#### Steps

1. **Install System Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql supervisor
```

2. **Create Application User**
```bash
sudo useradd -m -s /bin/bash plexchecker
sudo su - plexchecker
```

3. **Deploy Application**
```bash
cd /home/plexchecker
git clone <your-repo> plex_web  # or upload files
cd plex_web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

4. **Configure Environment**
```bash
nano .env
```
```
PLEX_BASE=http://your-plex:32400
PLEX_TOKEN=your_token
DJANGO_SECRET_KEY=generate_a_secure_random_key_here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/plexchecker
```

5. **Setup Database**
```bash
sudo -u postgres psql
CREATE DATABASE plexchecker;
CREATE USER plexchecker WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE plexchecker TO plexchecker;
\q
```

Update settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'plexchecker',
        'USER': 'plexchecker',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

6. **Run Migrations & Collect Static**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

7. **Create Gunicorn Service**
```bash
sudo nano /etc/supervisor/conf.d/plexchecker.conf
```
```ini
[program:plexchecker]
directory=/home/plexchecker/plex_web
command=/home/plexchecker/plex_web/venv/bin/gunicorn \
        --workers 3 \
        --bind unix:/home/plexchecker/plex_web/gunicorn.sock \
        plex_project.wsgi:application
user=plexchecker
autostart=true
autorestart=true
stderr_logfile=/var/log/plexchecker.err.log
stdout_logfile=/var/log/plexchecker.out.log
```

8. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/plexchecker
```
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/plexchecker/plex_web/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/home/plexchecker/plex_web/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

9. **Enable & Start Services**
```bash
sudo ln -s /etc/nginx/sites-available/plexchecker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start plexchecker
```

10. **Setup SSL (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -u 1000 plexchecker && chown -R plexchecker:plexchecker /app
USER plexchecker

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "plex_project.wsgi:application"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PLEX_BASE=${PLEX_BASE}
      - PLEX_TOKEN=${PLEX_TOKEN}
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=False
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/plexchecker
    depends_on:
      - db
    volumes:
      - static_volume:/app/staticfiles
      - cache_volume:/root
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=plexchecker
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/static:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  cache_volume:
```

#### Deploy
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

### Option 3: Platform-as-a-Service (Heroku, Railway, Render)

#### Heroku

1. **Install Heroku CLI & Login**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. **Create Heroku App**
```bash
heroku create your-plex-checker
```

3. **Add Postgres**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Configure Environment**
```bash
heroku config:set PLEX_BASE=http://your-plex:32400
heroku config:set PLEX_TOKEN=your_token
heroku config:set DJANGO_SECRET_KEY=your_secret_key
heroku config:set DJANGO_DEBUG=False
```

5. **Create Procfile**
```
web: gunicorn plex_project.wsgi --log-file -
```

6. **Create runtime.txt**
```
python-3.11.6
```

7. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a your-plex-checker
git push heroku main
heroku run python manage.py migrate
```

---

## Security Checklist

- [ ] Change SECRET_KEY to random value
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS/SSL
- [ ] Setup firewall (UFW/iptables)
- [ ] Use environment variables for secrets
- [ ] Restrict database access
- [ ] Regular security updates
- [ ] Setup monitoring/logging
- [ ] Backup database regularly
- [ ] Use strong passwords
- [ ] Implement rate limiting

## Performance Optimization

1. **Enable Caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database Connection Pooling**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'
        },
        'CONN_MAX_AGE': 600,
    }
}
```

3. **Gunicorn Workers**
```bash
# Workers = (2 × CPU cores) + 1
gunicorn --workers 5 --threads 2 plex_project.wsgi
```

## Monitoring

### Setup Logging
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/plexchecker/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Health Check Endpoint
Add to views.py:
```python
from django.http import JsonResponse

def health(request):
    return JsonResponse({'status': 'healthy'})
```

## Backup Strategy

```bash
# Database backup
pg_dump plexchecker > backup_$(date +%Y%m%d).sql

# Automated backups (crontab)
0 2 * * * /usr/bin/pg_dump plexchecker > /backups/plexchecker_$(date +\%Y\%m\%d).sql
```

## Maintenance

```bash
# Update application
cd /home/plexchecker/plex_web
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart plexchecker
```

## Troubleshooting

**502 Bad Gateway**
- Check Gunicorn is running: `sudo supervisorctl status`
- Check socket file exists: `ls -la gunicorn.sock`
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

**Static files not loading**
- Run collectstatic: `python manage.py collectstatic`
- Check Nginx configuration
- Verify STATIC_ROOT path

**Database connection errors**
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in settings.py
- Check pg_hba.conf permissions
