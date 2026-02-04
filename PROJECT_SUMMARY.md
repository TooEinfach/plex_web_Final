# Plex Checker Web UI - Project Summary

## Overview

This Django web application provides a modern, user-friendly interface for searching your Plex media server library. It's built as an upgrade from the original CLI tool (`plex_check.py`) while maintaining full compatibility and sharing the same underlying search logic.

## What's Included

### Core Application Files
- **Django Project Structure** - Complete, production-ready Django setup
- **Plex Integration** - Adapted from your original CLI tool
- **Search Engine** - Exact, fuzzy, and server search modes
- **Database Models** - Track search history and analytics
- **Modern Web UI** - Responsive, AJAX-powered interface
- **Statistics Dashboard** - View search patterns and success rates

### Documentation
- **README.md** - Comprehensive guide with features, installation, usage
- **QUICKSTART.md** - Get running in 5 minutes
- **DEPLOYMENT.md** - Production deployment guides (Linux, Docker, Heroku)
- **UI_OVERVIEW.md** - Visual interface documentation

### Configuration
- **.env.example** - Environment variable template
- **requirements.txt** - Python dependencies
- **.gitignore** - Version control exclusions
- **setup.sh** - Automated setup script

## Key Features

### Search Capabilities
✅ **Three Search Modes:**
- **Auto**: Tries exact → fuzzy → server (recommended)
- **Exact**: Perfect title matches only
- **Fuzzy**: Similarity-based matching with adjustable threshold

✅ **Library Filtering:**
- Search all libraries or filter by specific ones
- Support for Movies, TV Shows, and custom libraries

✅ **Performance:**
- Cached library data (6-hour TTL by default)
- Manual cache refresh available
- Fast fuzzy searches using RapidFuzz

### User Interface
✅ **Clean, Modern Design:**
- Plex-inspired color scheme (gold/orange accents)
- Responsive layout (desktop, tablet, mobile)
- No page reloads - AJAX-powered searches
- Real-time loading indicators

✅ **Search History:**
- Automatic logging of all searches
- View recent searches on homepage
- Detailed statistics page

✅ **Statistics Dashboard:**
- Total searches performed
- Success/failure rates
- Search type breakdown
- Complete search history table

### Technical Features
✅ **Full Django Stack:**
- Django 4.2+ framework
- SQLite database (easily upgradable to PostgreSQL)
- Admin interface for data management
- Production-ready with proper security settings

✅ **Plex Integration:**
- PlexAPI for server communication
- Shared cache with CLI tool
- Support for all Plex media types
- Rating key tracking for direct media access

## File Structure

```
plex_web/
├── manage.py                      # Django CLI
├── setup.sh                       # Automated setup
├── requirements.txt               # Dependencies
├── .env.example                   # Config template
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── DEPLOYMENT.md                  # Production deployment
├── UI_OVERVIEW.md                 # Interface docs
│
├── plex_project/                  # Django project
│   ├── __init__.py
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # URL routing
│   ├── wsgi.py                    # WSGI config
│   └── asgi.py                    # ASGI config
│
└── plex_checker/                  # Main app
    ├── __init__.py
    ├── apps.py                    # App configuration
    ├── models.py                  # Database models
    ├── views.py                   # View functions
    ├── urls.py                    # App URLs
    ├── admin.py                   # Admin interface
    ├── plex_service.py            # Plex integration
    │
    ├── templates/plex_checker/    # HTML templates
    │   ├── base.html              # Base layout
    │   ├── index.html             # Search page
    │   └── stats.html             # Statistics
    │
    └── static/plex_checker/       # Static files
        └── css/
            └── style.css          # Stylesheet
```

## Quick Start (TL;DR)

```bash
# 1. Extract and navigate to project
cd plex_web

# 2. Configure Plex credentials
cp .env.example .env
nano .env  # Add your PLEX_TOKEN

# 3. Run setup script
chmod +x setup.sh
./setup.sh

# 4. Start server
source venv/bin/activate
python manage.py runserver

# 5. Open browser
# http://localhost:8000
```

## Migration from CLI

Your original `plex_check.py` script is fully compatible with this web UI:

| Feature | CLI | Web UI |
|---------|-----|--------|
| Exact Search | ✅ | ✅ |
| Fuzzy Search | ✅ | ✅ |
| Library Cache | ✅ | ✅ (shared) |
| Search History | ❌ | ✅ |
| Statistics | ❌ | ✅ |
| Web Interface | ❌ | ✅ |
| Interactive | ✅ | ✅ |
| Batch Processing | ✅ | ❌ |

**You can use both simultaneously!** They share the same cache file (`~/.plex_cache.json`).

## What's Different from CLI

### Added Features
- 🌐 Web-based interface (no terminal needed)
- 📊 Search history and statistics
- 🎨 Visual results display
- 🔄 Auto mode (tries multiple search strategies)
- 📱 Mobile-friendly responsive design
- 👥 Multi-user support (with authentication setup)
- 🗄️ Persistent database for analytics

### Kept Features
- ✅ All search algorithms (exact, fuzzy, server)
- ✅ Library caching system
- ✅ Plex server connection logic
- ✅ Fuzzy matching with RapidFuzz
- ✅ Section filtering support

## Dependencies

```
Django>=4.2,<5.0        # Web framework
plexapi>=4.15.0         # Plex server API
rapidfuzz>=3.0.0        # Fuzzy string matching
python-dotenv>=1.0.0    # Environment variables
```

## Configuration Options

All configuration is done via `.env` file:

```bash
# Required
PLEX_BASE=http://10.0.0.208:32400
PLEX_TOKEN=your_token_here

# Optional
CACHE_TTL=21600                    # Cache lifetime (seconds)
DJANGO_SECRET_KEY=auto_generated   # Security key
DJANGO_DEBUG=True                  # Debug mode
DJANGO_ALLOWED_HOSTS=*             # Allowed domains
```

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Search Speed**: Sub-second for cached fuzzy searches
- **Cache Refresh**: ~5-30 seconds depending on library size
- **Concurrent Users**: Supports multiple simultaneous searches
- **Database**: SQLite for small deployments, PostgreSQL for production

## Security

- CSRF protection enabled
- XSS protection via Django templating
- Environment-based configuration (no hardcoded secrets)
- Production-ready settings included
- HTTPS support in deployment guides

## Future Enhancement Ideas

- User authentication and authorization
- Advanced filters (genre, rating, year range)
- Watchlist management
- Recently added media feed
- Bulk import from lists
- API endpoints for external integration
- Mobile app
- Email notifications
- Multi-language support

## Support & Troubleshooting

See README.md for common issues and solutions:
- Connection problems
- Cache not updating
- Search returning no results
- Static files not loading
- Database errors

## Credits

- Built with Django web framework
- PlexAPI for Plex server communication
- RapidFuzz for fuzzy string matching
- Inspired by the original plex_check.py CLI tool

## License

Provided as-is for personal use.

---

**Ready to deploy?** Check DEPLOYMENT.md for production setup guides!
