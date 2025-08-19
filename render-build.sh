#!/bin/bash

# Render.com Build Script
echo "🚀 Starting Düğün Drive deployment..."

# Force Python 3.9
echo "🐍 Setting Python version to 3.9..."
export PYTHON_VERSION=3.9.18

# Upgrade pip
echo "📦 Upgrading pip..."
python3.9 -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
python3.9 -m pip install -r requirements.txt

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

echo "✅ Build completed successfully!" 