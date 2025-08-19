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

echo "✅ Build completed successfully!" 