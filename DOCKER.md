# Docker Deployment Guide

This guide covers everything you need to know about running Temperature Trends Viz with Docker.

## Quick Start

The fastest way to run the application:

```bash
docker run -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest
```

Then open your browser and navigate to `http://localhost:8501`

> **Note**: All examples use `--name temperature-trends-viz` to provide a consistent container name for easy management. You can omit this parameter if you prefer Docker to generate a random name.

## Docker Hub Image

The official Docker image is available at:
- **Repository**: `medopaw/temperature-trends-viz`
- **Tags**: `latest`, version-specific tags (e.g., `1.0.0`)
- **Base Image**: Python 3.11 slim
- **Architecture**: linux/amd64

## Running Options

### 1. Direct Docker Run

```bash
# Run with default settings
docker run -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest

# Run in background (detached mode)
docker run -d -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest

# Run with custom port
docker run -p 8080:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest

# Run with environment variables
docker run -p 8501:8501 --name temperature-trends-viz \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  medopaw/temperature-trends-viz:latest
```

### 2. Docker Compose

Create a `docker-compose.yml` file or use the provided one:

```yaml
version: '3.8'

services:
  temperature-trends-viz:
    image: medopaw/temperature-trends-viz:latest
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Then run:

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## Building Your Own Image

If you want to build the image yourself:

```bash
# Clone the repository
git clone https://github.com/medopaw/temperature-trends-viz.git
cd temperature-trends-viz

# Build the image
docker build -t my-temperature-viz .

# Run your custom image
docker run -p 8501:8501 --name temperature-trends-viz my-temperature-viz
```

## Environment Variables

The following environment variables can be used to configure the application:

| Variable                               | Default   | Description                     |
| -------------------------------------- | --------- | ------------------------------- |
| `STREAMLIT_SERVER_PORT`                | `8501`    | Port the application listens on |
| `STREAMLIT_SERVER_ADDRESS`             | `0.0.0.0` | Address to bind to              |
| `STREAMLIT_SERVER_HEADLESS`            | `true`    | Run in headless mode            |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | `false`   | Disable usage statistics        |

## Health Check

The Docker image includes a health check endpoint:

```bash
# Check if the application is healthy
curl http://localhost:8501/_stcore/health
```

This endpoint returns `ok` when the application is running properly.

## Deployment Scripts

The repository includes helper scripts for deployment:

### Interactive Deployment

```bash
./docker-build-and-push.sh
```

This script will:
- Check Docker installation and login status
- Build the image with proper tags
- Test the image locally
- Ask for confirmation before pushing to Docker Hub
- Push to Docker Hub with version and latest tags

### Quick Deployment

```bash
./docker-quick-deploy.sh [version]
```

This script performs a quick build and push without interactive prompts.

Examples:
```bash
./docker-quick-deploy.sh          # Deploy as latest
./docker-quick-deploy.sh 1.0.0    # Deploy as version 1.0.0
```

## Production Deployment

For production deployments, consider:

### 1. Resource Limits

```bash
docker run -p 8501:8501 --name temperature-trends-viz \
  --memory=512m \
  --cpus=0.5 \
  medopaw/temperature-trends-viz:latest
```

### 2. Restart Policies

```bash
docker run -p 8501:8501 --name temperature-trends-viz \
  --restart=unless-stopped \
  medopaw/temperature-trends-viz:latest
```

### 3. Logging

```bash
docker run -p 8501:8501 --name temperature-trends-viz \
  --log-driver=json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  medopaw/temperature-trends-viz:latest
```

### 4. Security

The Docker image runs as a non-root user (`appuser`) for security.

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use a different port
   docker run -p 8502:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest
   ```

2. **Container won't start**
   ```bash
   # Check logs
   docker logs <container-id>
   ```

3. **Health check failing**
   ```bash
   # Check if the application is responding
   curl http://localhost:8501/_stcore/health
   ```

4. **Permission denied**
   ```bash
   # Make sure Docker daemon is running and you have permissions
   sudo docker run -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest
   ```

### Getting Help

If you encounter issues:
1. Check the container logs: `docker logs <container-name>`
2. Verify the health endpoint: `curl http://localhost:8501/_stcore/health`
3. Check if the port is available: `netstat -an | grep 8501`
4. Try running with a different port
5. Check the project's issue tracker on GitHub

## Image Details

### Technical Specifications
- **Base Image**: `python:3.11-slim`
- **Working Directory**: `/app`
- **Exposed Port**: `8501` (Streamlit default)
- **User**: `appuser` (non-root for security)
- **Health Check**: Built-in endpoint monitoring
- **Multi-stage Build**: Optimized for size and security
- **Architecture**: `linux/amd64`

### Image Optimization Features
- **Slim Base Image**: Uses `python:3.11-slim` for smaller attack surface
- **Multi-stage Build**: Separates build and runtime environments
- **Dependency Optimization**: Uses `uv` for fast dependency resolution
- **Cache Cleanup**: Removes apt caches and build dependencies
- **Minimal Layers**: Optimized Dockerfile structure

### Security Features
- **Non-root Execution**: Runs as `appuser` for enhanced security
- **Minimal Base**: Reduced attack surface with slim image
- **No Secrets**: No sensitive data baked into the image
- **Health Monitoring**: Built-in health check endpoint

The image is built using multi-stage builds to minimize size while including all necessary dependencies. The final image size is approximately 900MB including all Python dependencies.

## Deployment to Docker Hub

### Prerequisites for Deployment

1. **Docker installed and running**
   ```bash
   docker --version
   docker info
   ```

2. **Docker Hub account**
   - Create an account at [hub.docker.com](https://hub.docker.com)
   - Note your username (used in image tags)

3. **Repository cloned**
   ```bash
   git clone https://github.com/medopaw/temperature-trends-viz.git
   cd temperature-trends-viz
   ```

### Quick Deployment Options

#### Option 1: Using the Interactive Script

```bash
# Make script executable
chmod +x docker-build-and-push.sh

# Run the interactive deployment script
./docker-build-and-push.sh
```

This script will:
- Check Docker installation and login status
- Build the image with proper tags
- Test the image locally
- Ask for confirmation before pushing
- Push to Docker Hub

#### Option 2: Using the Quick Deploy Script

```bash
# Make script executable
chmod +x docker-quick-deploy.sh

# Deploy as latest
./docker-quick-deploy.sh

# Deploy with specific version
./docker-quick-deploy.sh 1.0.0
```

### Manual Deployment Process

#### Step 1: Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

#### Step 2: Build the Image

```bash
# Build with version tag
docker build -t medopaw/temperature-trends-viz:1.0.0 .

# Tag as latest
docker tag medopaw/temperature-trends-viz:1.0.0 medopaw/temperature-trends-viz:latest
```

#### Step 3: Test the Image

```bash
# Run the container
docker run -d --name test-container -p 8502:8501 medopaw/temperature-trends-viz:1.0.0

# Wait for startup
sleep 10

# Test health endpoint
curl -f http://localhost:8502/_stcore/health

# Clean up
docker stop test-container
docker rm test-container
```

#### Step 4: Push to Docker Hub

```bash
# Push version tag
docker push medopaw/temperature-trends-viz:1.0.0

# Push latest tag
docker push medopaw/temperature-trends-viz:latest
```

### Deployment Verification

After pushing, verify the deployment:

1. **Check Docker Hub**
   - Visit [hub.docker.com/r/medopaw/temperature-trends-viz](https://hub.docker.com/r/medopaw/temperature-trends-viz)
   - Verify tags are present

2. **Test Pull and Run**
   ```bash
   # Remove local images
   docker rmi medopaw/temperature-trends-viz:latest
   docker rmi medopaw/temperature-trends-viz:1.0.0

   # Pull and run from Docker Hub
   docker run -p 8501:8501 --name temperature-trends-viz medopaw/temperature-trends-viz:latest
   ```

3. **Test Application**
   - Open browser to `http://localhost:8501`
   - Verify application loads and functions correctly

## Version Management

### Semantic Versioning

Use semantic versioning for releases:
- `1.0.0` - Major release
- `1.1.0` - Minor release (new features)
- `1.0.1` - Patch release (bug fixes)

### Tagging Strategy

Always create both version-specific and latest tags:

```bash
# For version 1.0.0
docker build -t medopaw/temperature-trends-viz:1.0.0 .
docker tag medopaw/temperature-trends-viz:1.0.0 medopaw/temperature-trends-viz:latest

# Push both tags
docker push medopaw/temperature-trends-viz:1.0.0
docker push medopaw/temperature-trends-viz:latest
```

## Automated Deployment

### GitHub Actions (Future Enhancement)

Consider setting up GitHub Actions for automated deployment:

```yaml
# .github/workflows/docker-publish.yml
name: Docker Publish

on:
  push:
    tags: ['v*']
  release:
    types: [published]

jobs:
  push_to_registry:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: medopaw/temperature-trends-viz

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## Deployment Troubleshooting

### Common Deployment Issues

1. **Authentication Failed**
   ```bash
   # Re-login to Docker Hub
   docker logout
   docker login
   ```

2. **Build Fails**
   ```bash
   # Clean Docker cache
   docker system prune -a

   # Rebuild without cache
   docker build --no-cache -t medopaw/temperature-trends-viz:latest .
   ```

3. **Push Fails**
   ```bash
   # Check image exists
   docker images | grep temperature-trends-viz

   # Check login status
   docker info | grep Username
   ```

4. **Image Too Large**
   ```bash
   # Check image size
   docker images medopaw/temperature-trends-viz

   # The multi-stage build should keep it under 1GB
   ```

## Security Considerations

1. **Non-root User**: The image runs as `appuser` (non-root)
2. **Minimal Base**: Uses `python:3.11-slim` for smaller attack surface
3. **No Secrets**: No sensitive data is baked into the image
4. **Health Checks**: Built-in health monitoring

## Maintenance

### Regular Updates

1. **Update Dependencies**
   ```bash
   # Update uv.lock
   uv sync --upgrade

   # Rebuild and test
   docker build -t medopaw/temperature-trends-viz:latest .
   ```

2. **Security Updates**
   ```bash
   # Rebuild with latest base image
   docker build --pull -t medopaw/temperature-trends-viz:latest .
   ```

3. **Version Bumps**
   - Update version in `pyproject.toml`
   - Create new git tag
   - Build and push new version

### Maintenance Checklist

✅ **Build Test**: Image builds successfully
✅ **Runtime Test**: Container starts properly
✅ **Health Check**: Application responds correctly
✅ **Port Mapping**: Port 8501 accessible
✅ **Multi-stage Build**: Image size optimized

## Support

For deployment and Docker issues:
1. Check the container logs: `docker logs <container-name>`
2. Verify health: `curl http://localhost:8501/_stcore/health`
3. Check if the port is available: `netstat -an | grep 8501`
4. Try running with a different port
5. Check the project's issue tracker on GitHub
