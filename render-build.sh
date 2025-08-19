#!/bin/bash

# Render.com Build Script
echo "🚀 Starting Düğün Drive deployment..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
echo "⚙️ Setting up environment..."
cp env.production .env

# Copy credentials file
echo "🔐 Setting up Google Drive credentials..."
cp credentials.json /opt/render/project/src/credentials.json

echo "✅ Build completed successfully!" 