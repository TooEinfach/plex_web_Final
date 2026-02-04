# TrueNAS Scale Deployment Guide

## Overview

TrueNAS Scale supports Docker containers natively, making it perfect for deploying the Plex Checker web app. You have three deployment options:

---

## Option 1: Docker Compose (Easiest)

### Prerequisites
- TrueNAS Scale 22.02 or newer
- SSH access to your TrueNAS server
- Your Plex token

### Step-by-Step Instructions

#### 1. Enable SSH on TrueNAS
1. Go to **System Settings** → **Services**
2. Enable **SSH** service
3. Note your TrueNAS IP address

#### 2. SSH into TrueNAS
```bash
ssh admin@your-truenas-ip
```

#### 3. Create Project Directory
```bash
# Create a directory in your pool (replace 'tank' with your pool name)
mkdir -p /mnt/tank/apps/plex-checker
cd /mnt/tank/apps/plex-checker
```

#### 4. Upload Project Files
On your local machine, upload the project:
```bash
# Extract the zip file first
unzip plex_web.zip

# Copy to TrueNAS (from your local machine)
scp -r plex_web/* admin@your-truenas-ip:/mnt/tank/apps/plex-checker/
scp Dockerfile admin@your-truenas-ip:/mnt/tank/apps/plex-checker/
scp docker-compose.yml admin@your-truenas-ip:/mnt/tank/apps/plex-checker/
```

Or use WinSCP/FileZilla if you prefer a GUI.

#### 5. Create Environment File
Back on TrueNAS SSH:
```bash
cd /mnt/tank/apps/plex-checker
nano .env
```

Add your configuration:
```env
PLEX_BASE=http://your-plex-ip:32400
PLEX_TOKEN=your_actual_plex_token_here
DJANGO_SECRET_KEY=generate-a-random-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=truenas-ip,truenas-hostname,*
CACHE_TTL=21600
```

Save and exit (Ctrl+X, Y, Enter)

#### 6. Build and Start Container
```bash
docker-compose up -d
```

#### 7. Check Container Status
```bash
docker-compose ps
docker-compose logs -f
```

#### 8. Access the Application
Open your browser to: `http://your-truenas-ip:8000`

### Managing the Container

```bash
# Stop the container
docker-compose down

# Restart the container
docker-compose restart

# View logs
docker-compose logs -f

# Update the application
git pull  # or re-upload files
docker-compose build --no-cache
docker-compose up -d

# Shell into container
docker-compose exec plex-checker bash
```

---

## Option 2: TrueNAS Apps (Custom App)

TrueNAS Scale has a built-in Apps feature (based on Helm charts). While there's no pre-made chart for Plex Checker, you can create a custom app.

### Step 1: Prepare the Image

First, build and push to Docker Hub (from your local machine):

```bash
cd plex_web
docker build -t yourusername/plex-checker:latest .
docker login
docker push yourusername/plex-checker:latest
```

### Step 2: Install via TrueNAS UI

1. Go to **Apps** in TrueNAS Scale
2. Click **Discover Apps** → **Custom App**
3. Fill in the details:

**Application Name:** `plex-checker`

**Image Configuration:**
- Image Repository: `yourusername/plex-checker`
- Image Tag: `latest`
- Image Pull Policy: `IfNotPresent`

**Container Configuration:**
- Container Port: `8000`
- Node Port: `30800` (or any available port)

**Environment Variables:**
Add these variables:
```
PLEX_BASE=http://your-plex-ip:32400
PLEX_TOKEN=your_token
DJANGO_SECRET_KEY=your_secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
```

**Storage:**
- Add Host Path Volume:
  - Host Path: `/mnt/tank/apps/plex-checker/db`
  - Mount Path: `/app`
  - Type: `Directory`

4. Click **Install**

5. Access at: `http://truenas-ip:30800`

---

## Option 3: Using TrueNAS Jails (Legacy Method)

If you're using TrueNAS Core (FreeBSD-based), you'd use Jails. But since you mentioned TrueNAS Scale, Docker is the recommended approach.

---

## Network Configuration

### Accessing from Other Devices

By default, the app will be accessible at `http://truenas-ip:8000`. If you want a custom domain:

#### Option A: Reverse Proxy (Recommended)

Install Nginx Proxy Manager as another Docker container:

```yaml
# Add to docker-compose.yml or create separate compose file
services:
  nginx-proxy-manager:
    image: jc21/nginx-proxy-manager:latest
    ports:
      - "80:80"
      - "443:443"
      - "81:81"
    volumes:
      - nginx-data:/data
      - nginx-letsencrypt:/etc/letsencrypt
    restart: unless-stopped

volumes:
  nginx-data:
  nginx-letsencrypt:
```

Then configure a proxy host pointing to `plex-checker:8000`

#### Option B: Direct DNS

Add a DNS entry in your router pointing `plex-checker.local` to your TrueNAS IP.

---

## Connecting to Plex Server

### If Plex is on the Same TrueNAS Server

Use the TrueNAS IP address:
```env
PLEX_BASE=http://192.168.1.100:32400
```

### If Plex is in a Docker Container on TrueNAS

You have two options:

**Option 1: Use Docker Network**
If Plex is in a container, add both to the same Docker network:

```yaml
services:
  plex-checker:
    networks:
      - plex-network
  
  # If Plex is also in Docker
  plex:
    networks:
      - plex-network

networks:
  plex-network:
    external: true  # If Plex network already exists
```

Then use:
```env
PLEX_BASE=http://plex:32400
```

**Option 2: Use Host IP**
```env
PLEX_BASE=http://192.168.1.100:32400
```

### If Plex is on Another Server

Just use that server's IP:
```env
PLEX_BASE=http://192.168.1.50:32400
```

---

## Data Persistence

The docker-compose.yml already includes volumes for:
- **Database**: Stores search history
- **Cache**: Stores Plex library cache

These persist across container restarts/updates.

### Backup Your Data

```bash
# Backup database
docker-compose exec plex-checker python manage.py dumpdata > backup.json

# Or copy the SQLite file directly
docker cp plex-checker:/app/db.sqlite3 ./backup.db
```

---

## Security Considerations

### 1. Change Default Secret Key
Generate a secure secret key:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Set Allowed Hosts
Restrict which domains can access:
```env
DJANGO_ALLOWED_HOSTS=truenas.local,192.168.1.100
```

### 3. Enable HTTPS
Use Nginx Proxy Manager with Let's Encrypt for free SSL certificates.

### 4. Restrict Network Access
Use TrueNAS firewall or Docker network isolation to limit access.

---

## Performance Tuning

### Adjust Workers
For better performance, modify the Dockerfile CMD:
```dockerfile
CMD gunicorn --bind 0.0.0.0:8000 --workers 5 --threads 2 plex_project.wsgi:application
```

Rule: workers = (2 × CPU cores) + 1

### Use PostgreSQL Instead of SQLite
For production use, add PostgreSQL:

```yaml
services:
  plex-checker:
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://plexuser:password@db:5432/plexchecker
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=plexchecker
      - POSTGRES_USER=plexuser
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs

# Check if port 8000 is already in use
netstat -an | grep 8000

# Try different port
# Edit docker-compose.yml: "8001:8000"
```

### Can't Connect to Plex
```bash
# Test from within container
docker-compose exec plex-checker bash
curl http://your-plex-ip:32400

# Check if PLEX_TOKEN is correct
docker-compose exec plex-checker env | grep PLEX
```

### Database Locked
```bash
# Stop container
docker-compose down

# Remove lock
docker volume inspect plex-checker-db
# Find mount point and delete .lock file

# Restart
docker-compose up -d
```

### Static Files Not Loading
```bash
# Rebuild and collect static
docker-compose exec plex-checker python manage.py collectstatic --noinput
docker-compose restart
```

---

## Updating the Application

### Method 1: Rebuild Container
```bash
cd /mnt/tank/apps/plex-checker

# Stop current container
docker-compose down

# Update files (upload new version or git pull)
# ...

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Method 2: Direct Update (No Downtime)
```bash
# Update code
docker-compose exec plex-checker bash
cd /app
# Make changes

# Restart just the app
docker-compose restart
```

---

## Monitoring

### View Real-time Logs
```bash
docker-compose logs -f
```

### Check Resource Usage
```bash
docker stats plex-checker
```

### TrueNAS Dashboard
Check container health in **Apps** section of TrueNAS UI.

---

## Alternative: Run Directly on TrueNAS (Not Recommended)

You could install Python directly on TrueNAS Scale and run it, but this is **not recommended** because:
- System updates might break it
- No isolation from host system
- Harder to manage and update
- Containers are the TrueNAS Scale way

---

## Quick Reference Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Shell access
docker-compose exec plex-checker bash

# Update
docker-compose pull && docker-compose up -d

# Backup database
docker-compose exec plex-checker python manage.py dumpdata > backup.json

# Check status
docker-compose ps
```

---

## Getting Help

If you run into issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables: `docker-compose config`
3. Test Plex connection: `curl http://plex-ip:32400`
4. Check container health: `docker inspect plex-checker`

---

**Recommended Setup:** Use Option 1 (Docker Compose) - it's the easiest and most maintainable for TrueNAS Scale!
