#!/bin/bash

# Quick deployment script for Temperature Trends Viz
# This script builds and pushes to Docker Hub in one command

set -e

# Default configuration
DOCKER_USERNAME="${DOCKER_USERNAME:-medopaw}"
IMAGE_NAME="temperature-trends-viz"
VERSION="${1:-latest}"

echo "🚀 Quick Deploy: $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

# Build
echo "📦 Building image..."
docker build -t "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION" .

# Tag as latest if not already latest
if [ "$VERSION" != "latest" ]; then
    docker tag "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION" "$DOCKER_USERNAME/$IMAGE_NAME:latest"
fi

# Push
echo "⬆️  Pushing to Docker Hub..."
docker push "$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"

if [ "$VERSION" != "latest" ]; then
    docker push "$DOCKER_USERNAME/$IMAGE_NAME:latest"
fi

echo "✅ Deployment complete!"
echo "🌐 Run with: docker run -p 8501:8501 --name temperature-trends-viz $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
