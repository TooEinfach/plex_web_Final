# Quick Start Guide

## 5-Minute Setup

### 1. Get Your Plex Token

1. Go to https://app.plex.tv
2. Play any media item
3. Click ⋯ (three dots) → "Get Info"
4. Click "View XML"
5. Look in the URL for `X-Plex-Token=XXXXXXXXXX`
6. Copy the token value

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Add your token:
```
PLEX_TOKEN=your_token_here
PLEX_BASE=http://your-plex-ip:32400
```

### 3. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

OR manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### 4. Start Server

```bash
python manage.py runserver
```

### 5. Open Browser

Navigate to: http://localhost:8000

## First Search

1. Type a movie/show name (e.g., "The Matrix")
2. Select "Auto" search mode
3. Click "Search"

## Common Issues

**"PLEX_TOKEN not configured"**
- Edit `.env` file and add your token

**"Connection refused"**
- Check `PLEX_BASE` URL in `.env`
- Ensure Plex server is running

**"No results found"**
- Click "Refresh Cache" button
- Try lowering fuzzy threshold to 70

## Tips

- Use **Auto** mode for best results
- Click **Refresh Cache** after adding new media to Plex
- Check **Stats** page to see search history
- Use **Fuzzy** mode for partial title matches

## Next Steps

- Create admin user: `python manage.py createsuperuser`
- Access admin panel: http://localhost:8000/admin
- Customize settings in `plex_project/settings.py`
