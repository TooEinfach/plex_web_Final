# Plex Checker Web UI

A Django web application for searching your Plex media server library with exact matching, fuzzy matching, and search history tracking.

## Features

- 🔍 **Multiple Search Modes**
  - Exact match search
  - Fuzzy matching with configurable threshold
  - Auto mode (tries exact → fuzzy → server search)
  
- 📚 **Library Management**
  - Search across all libraries or select specific ones
  - Cached library data for fast searches (6-hour default TTL)
  - Manual cache refresh option

- 📊 **Statistics & History**
  - Track all searches with timestamps
  - View success rates and search patterns
  - Browse recent search history

- 🎨 **Modern UI**
  - Clean, responsive design
  - Real-time search results
  - AJAX-powered for smooth user experience

## Installation

### Prerequisites

- Python 3.8 or higher
- Plex Media Server with API access
- Plex authentication token

### Setup

1. **Clone or copy the project directory**
   ```bash
   cd plex_web
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your Plex credentials:
   ```
   PLEX_BASE=http://your-plex-server:32400
   PLEX_TOKEN=your_plex_token_here
   ```

   **Finding your Plex token:**
   - Log into Plex Web App
   - Play any media item
   - Click the three dots (⋯) → "Get Info"
   - Click "View XML"
   - Look for `X-Plex-Token` in the URL

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Usage

### Basic Search

1. Navigate to the home page
2. Enter a movie or TV show title
3. Select search mode:
   - **Auto**: Recommended - tries exact match first, then fuzzy, then server search
   - **Exact**: Only returns perfect title matches
   - **Fuzzy**: Uses similarity scoring (adjust threshold as needed)
4. Optionally select a specific library to search
5. Click "Search"

### Search Options

- **Library Filter**: Limit search to Movies, TV Shows, or other libraries
- **Fuzzy Threshold**: Set minimum similarity score (0-100, default 85)
  - Higher = more strict matching
  - Lower = more lenient matching

### Cache Management

The app caches your Plex library for faster searches:
- Cache refreshes automatically every 6 hours
- Click "Refresh Cache" to manually update
- Useful after adding new media to Plex

### Statistics

Visit the Stats page to see:
- Total searches performed
- Success/failure rates
- Search type breakdown
- Recent search history

## Project Structure

```
plex_web/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── plex_project/                  # Django project settings
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # Root URL routing
│   └── wsgi.py                    # WSGI config
├── plex_checker/                  # Main application
│   ├── models.py                  # Database models (SearchHistory)
│   ├── views.py                   # View functions (search, stats)
│   ├── urls.py                    # App URL routing
│   ├── plex_service.py            # Plex API integration
│   ├── templates/plex_checker/    # HTML templates
│   │   ├── base.html              # Base template
│   │   ├── index.html             # Search page
│   │   └── stats.html             # Statistics page
│   └── static/plex_checker/       # Static files
│       └── css/
│           └── style.css          # Main stylesheet
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PLEX_BASE` | Plex server URL | `http://10.0.0.208:32400` |
| `PLEX_TOKEN` | Plex authentication token | Required |
| `CACHE_TTL` | Cache lifetime in seconds | `21600` (6 hours) |
| `DJANGO_SECRET_KEY` | Django secret key | Auto-generated |
| `DJANGO_DEBUG` | Enable debug mode | `True` |

### Django Settings

Edit `plex_project/settings.py` to customize:
- Database configuration (defaults to SQLite)
- Allowed hosts
- Cache settings
- Logging configuration

## How It Works

### Search Flow

1. **Exact Search**: Queries Plex API for exact title matches
2. **Fuzzy Search**: Uses RapidFuzz library to compare against cached titles
3. **Server Search**: Falls back to Plex's built-in search for mixed results

### Caching System

- Library data cached in `~/.plex_cache.json`
- Includes title, year, type, and rating key for all media
- Significantly speeds up fuzzy searches
- Auto-refreshes based on TTL

### Database

Uses SQLite to store:
- Search history
- Success/failure tracking
- Search type analytics

## Migration from CLI

This web app is fully compatible with your original `plex_check.py` script:

- Same Plex connection logic
- Same search algorithms
- Same caching mechanism
- Shared cache file (`~/.plex_cache.json`)

You can continue using both the CLI and web interface simultaneously.

## Deployment

### Production Checklist

1. **Set secure secret key**
   ```python
   # settings.py
   SECRET_KEY = 'your-secure-random-key-here'
   ```

2. **Disable debug mode**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

3. **Use production database**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           # ... PostgreSQL config
       }
   }
   ```

4. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

5. **Use production server**
   - Gunicorn: `gunicorn plex_project.wsgi:application`
   - uWSGI: `uwsgi --http :8000 --module plex_project.wsgi`

6. **Set up reverse proxy** (Nginx/Apache)

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "plex_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Troubleshooting

### Can't connect to Plex

- Verify `PLEX_BASE` URL is correct
- Check firewall allows access to Plex port
- Ensure `PLEX_TOKEN` is valid
- Try accessing Plex Web App directly

### Search returns no results

- Click "Refresh Cache" to update library data
- Try lowering fuzzy threshold
- Check if media exists in Plex Web App
- Verify library selection (all vs. specific)

### Cache not updating

- Check write permissions on home directory
- Look for errors in console/logs
- Manually delete `~/.plex_cache.json` and refresh

### CSS not loading

- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings
- Verify static files middleware is enabled

## Future Enhancements

Potential features to add:
- User authentication
- Advanced filters (genre, rating, etc.)
- Watchlist integration
- Recently added media feed
- Mobile app
- Export search results

## License

This project builds upon the original `plex_check.py` CLI tool and is provided as-is for personal use.

## Credits

- Built with Django web framework
- Uses PlexAPI for Plex server communication
- RapidFuzz for fuzzy string matching
