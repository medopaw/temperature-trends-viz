#!/bin/bash

# Docker build and push script for Temperature Trends Viz
# This script builds the Docker image and pushes it to Docker Hub

set -e  # Exit on any error

# Configuration
DOCKER_USERNAME="${DOCKER_USERNAME:-medopaw}"
IMAGE_NAME="temperature-trends-viz"
VERSION="${VERSION:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    log_success "Docker is running"
}

# Check if logged in to Docker Hub
check_docker_login() {
    if ! docker info | grep -q "Username: $DOCKER_USERNAME"; then
        log_warning "Not logged in to Docker Hub as $DOCKER_USERNAME"
        log_info "Please run: docker login"
        read -p "Do you want to login now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker login
        else
            log_error "Please login to Docker Hub first"
            exit 1
        fi
    fi
    log_success "Logged in to Docker Hub as $DOCKER_USERNAME"
}

# Build the Docker image
build_image() {
    local full_image_name="$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    local latest_image_name="$DOCKER_USERNAME/$IMAGE_NAME:latest"
    
    log_info "Building Docker image: $full_image_name"
    
    # Build with version tag
    docker build -t "$full_image_name" .
    
    # Also tag as latest if version is not latest
    if [ "$VERSION" != "latest" ]; then
        docker tag "$full_image_name" "$latest_image_name"
        log_success "Tagged image as both $VERSION and latest"
    else
        log_success "Built image: $full_image_name"
    fi
}

# Push the Docker image
push_image() {
    local full_image_name="$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    local latest_image_name="$DOCKER_USERNAME/$IMAGE_NAME:latest"
    
    log_info "Pushing Docker image: $full_image_name"
    docker push "$full_image_name"
    log_success "Pushed: $full_image_name"
    
    # Push latest tag if version is not latest
    if [ "$VERSION" != "latest" ]; then
        log_info "Pushing Docker image: $latest_image_name"
        docker push "$latest_image_name"
        log_success "Pushed: $latest_image_name"
    fi
}

# Test the image locally
test_image() {
    local full_image_name="$DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    
    log_info "Testing the built image locally..."
    
    # Run container in background
    local container_id=$(docker run -d -p 8502:8501 --name temperature-trends-viz-test "$full_image_name")
    
    # Wait a bit for the container to start
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:8502/_stcore/health >/dev/null 2>&1; then
        log_success "Image test passed - application is responding"
    else
        log_error "Image test failed - application is not responding"
        docker logs "$container_id"
        docker stop "$container_id" >/dev/null 2>&1
        docker rm "$container_id" >/dev/null 2>&1
        exit 1
    fi
    
    # Clean up
    docker stop "$container_id" >/dev/null 2>&1
    docker rm "$container_id" >/dev/null 2>&1
    log_success "Test cleanup completed"
}

# Main execution
main() {
    log_info "Starting Docker build and push process..."
    log_info "Image: $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
    
    # Pre-flight checks
    check_docker
    check_docker_login
    
    # Build and test
    build_image
    test_image
    
    # Ask for confirmation before pushing
    echo
    log_warning "Ready to push to Docker Hub"
    read -p "Do you want to continue with the push? (y/n): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        push_image
        echo
        log_success "🎉 Successfully built and pushed Docker image!"
        log_info "You can now run the application with:"
        log_info "  docker run -p 8501:8501 --name temperature-trends-viz $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
        log_info "Or use docker-compose:"
        log_info "  docker-compose up -d"
    else
        log_info "Push cancelled by user"
    fi
}

# Show usage if help requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [VERSION]"
    echo ""
    echo "Environment variables:"
    echo "  DOCKER_USERNAME - Docker Hub username (default: medopaw)"
    echo "  VERSION         - Image version tag (default: latest)"
    echo ""
    echo "Examples:"
    echo "  $0              # Build and push as latest"
    echo "  VERSION=1.0.0 $0  # Build and push as version 1.0.0"
    echo "  $0 1.0.0        # Build and push as version 1.0.0"
    exit 0
fi

# Override version if provided as argument
if [ -n "$1" ]; then
    VERSION="$1"
fi

# Run main function
main
