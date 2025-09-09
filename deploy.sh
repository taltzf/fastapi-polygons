#!/bin/sh
set -e

echo "🛠 Building Docker images..."
docker-compose build

echo "🚀 Starting containers (with migrations)..."
docker-compose up --remove-orphans --build -d

echo "✅ Containers are running."
docker-compose ps

echo "Streaming FastAPI logs (Ctrl+C to exit)..."
docker-compose logs -f fastapi_app