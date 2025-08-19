#!/bin/bash

# Render.com Build Script
echo "🚀 Starting Düğün Drive deployment..."

# Clear pip cache
echo "🧹 Clearing pip cache..."
pip cache purge

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies with no cache
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Copy environment file
echo "⚙️ Setting up environment..."
cp env.production .env

# Copy credentials file
echo "🔐 Setting up Google Drive credentials..."
cp credentials.json /opt/render/project/src/credentials.json
cp credentials.json credentials.json.bak

# Clear any cached files
echo "🧹 Clearing cache..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Set all environment variables automatically
echo "🔧 Setting all environment variables automatically..."
export PYTHON_VERSION=3.13.0
export ENVIRONMENT=production
export GOOGLE_CREDENTIALS_FILE=credentials.json
export GOOGLE_TOKEN_FILE=token.json
export API_TITLE="Düğün Drive API"
export API_VERSION=1.0.0
export API_DESCRIPTION="Düğün Drive integration API"
export ALLOWED_ORIGINS='["http://localhost:3000","http://localhost:8080","http://localhost:8000","http://127.0.0.1:8000","https://*.netlify.app","https://*.onrender.com","https://dugun-drive.netlify.app","https://dugun-drive-api.onrender.com"]'

echo "✅ Build completed successfully!" 