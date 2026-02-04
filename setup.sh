#!/bin/bash
# Setup script for Plex Checker Web UI

echo "🎬 Plex Checker Web UI - Setup Script"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your PLEX_TOKEN"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your PLEX_TOKEN"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run server: python manage.py runserver"
echo "4. Open browser to: http://localhost:8000"
echo ""
echo "Optional: Create admin user with: python manage.py createsuperuser"
