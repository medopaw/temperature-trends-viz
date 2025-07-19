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
