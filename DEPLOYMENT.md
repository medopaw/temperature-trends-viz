# Deployment Instructions

This document provides step-by-step instructions for deploying Temperature Trends Viz to Docker Hub.

## Prerequisites

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

## Quick Deployment

### Option 1: Using the Interactive Script

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

### Option 2: Using the Quick Deploy Script

```bash
# Make script executable
chmod +x docker-quick-deploy.sh

# Deploy as latest
./docker-quick-deploy.sh

# Deploy with specific version
./docker-quick-deploy.sh 1.0.0
```

## Manual Deployment

### Step 1: Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

### Step 2: Build the Image

```bash
# Build with version tag
docker build -t medopaw/temperature-trends-viz:1.0.0 .

# Tag as latest
docker tag medopaw/temperature-trends-viz:1.0.0 medopaw/temperature-trends-viz:latest
```

### Step 3: Test the Image

```bash
# Run the container
docker run -d --name temperature-trends-viz -p 8502:8501 medopaw/temperature-trends-viz:1.0.0

# Wait for startup
sleep 10

# Test health endpoint
curl -f http://localhost:8502/_stcore/health

# Clean up
docker stop test-container
docker rm test-container
```

### Step 4: Push to Docker Hub

```bash
# Push version tag
docker push medopaw/temperature-trends-viz:1.0.0

# Push latest tag
docker push medopaw/temperature-trends-viz:latest
```

## Verification

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

## Troubleshooting

### Common Issues

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
   
   # The multi-stage build should keep it under 200MB
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

### Next Steps for Production

1. **Push to Docker Hub**: Use provided scripts to push images
2. **Set up CI/CD**: Consider GitHub Actions for automated deployment
3. **Monitoring**: Set up logging and monitoring in production
4. **Scaling**: Add load balancing and multiple instances as needed

## Support

For deployment issues:
1. Check the logs: `docker logs <container-name>`
2. Verify health: `curl http://localhost:8501/_stcore/health`
3. Check the GitHub issues page
4. Review this deployment guide
