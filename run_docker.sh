#!/bin/bash

# Google Shopping Scraper Docker Runner
# This script builds and runs the scraper in Docker

set -e

echo "🐳 Google Shopping Scraper - Docker Edition"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << EOF
# LambdaTest Credentials (optional for Docker version)
LAMBDATEST_USERNAME=your_lambdatest_username
LAMBDATEST_ACCESS_KEY=your_lambdatest_access_key

# Docker Configuration
PYTHONUNBUFFERED=1
EOF
    echo "📝 Please edit .env file with your credentials if needed."
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

# Run the scraper
echo "🚀 Starting scraper..."
docker-compose up scraper

# Show results
echo "📊 Scraping completed!"
echo "📁 Results saved in ./data/scraped_results.json"

# Optional: Show the results
if [ -f "data/scraped_results.json" ]; then
    echo ""
    echo "📋 Results preview:"
    echo "=================="
    head -20 data/scraped_results.json
    echo "..."
fi

echo ""
echo "✅ Done! Check ./data/ for results and ./logs/ for logs." 