# Docker Guide for MCP Persona Server

## Overview

This guide explains how to build and run the MCP Persona Server using Docker. Docker provides a consistent, isolated environment for running the server across different platforms.

## Prerequisites

- **Docker**: Install Docker Desktop or Docker Engine
- **Docker Compose**: Usually included with Docker Desktop
- **Git**: To clone the repository

## Quick Start

### 1. **Build the Docker Image**

```bash
# Build the production image
./scripts/docker-build.sh

# Or build with a specific tag
./scripts/docker-build.sh --tag v1.0.0

# Build development image
./scripts/docker-build.sh --dev
```

### 2. **Run the Container**

```bash
# Run with persistent data storage
./scripts/docker-run.sh

# Run with temporary storage (data will be lost when container stops)
./scripts/docker-run.sh --no-persist

# Run with a specific image tag
./scripts/docker-run.sh --tag v1.0.0
```

### 3. **Using Docker Compose**

```bash
# Start the service
docker-compose up

# Start in background
docker-compose up -d

# Start development service
docker-compose --profile dev up

# Stop the service
docker-compose down
```

## Docker Configuration

### **Dockerfile Features**

- **Base Image**: Python 3.11 slim for smaller size
- **Security**: Non-root user (`mcp_user`)
- **Optimization**: Multi-stage build with dependency caching
- **Environment**: Proper Python path and environment variables

### **Volume Mounts**

- **`./personas:/app/personas`**: Persistent persona storage
- **`./config.json:/app/config.json:ro`**: Read-only configuration

### **Environment Variables**

- `PERSONA_STORAGE_PATH`: Path to persona storage directory
- `PYTHONPATH`: Python module search path
- `PYTHONUNBUFFERED`: Unbuffered Python output for logging

## Usage Examples

### **Basic Usage**

```bash
# Build and run in one command
./scripts/docker-build.sh && ./scripts/docker-run.sh
```

### **Development Workflow**

```bash
# Build development image
./scripts/docker-build.sh --dev

# Run with source code mounted for development
docker-compose --profile dev up
```

### **Production Deployment**

```bash
# Build production image
./scripts/docker-build.sh --tag production

# Run with persistent storage
./scripts/docker-run.sh --tag production
```

### **Testing Different Configurations**

```bash
# Test with temporary storage
./scripts/docker-run.sh --no-persist

# Test with custom container name
./scripts/docker-run.sh --name my-persona-server
```

## Integration with Claude Desktop

### **Claude Desktop Configuration**

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "persona-server": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "/path/to/your/personas:/app/personas", "mcp-persona-server:latest"]
    }
  }
}
```

### **Alternative: Using Docker Compose**

```json
{
  "mcpServers": {
    "persona-server": {
      "command": "docker-compose",
      "args": ["run", "--rm", "mcp-persona-server"]
    }
  }
}
```

## Advanced Configuration

### **Custom Configuration**

Create a custom `config.json`:

```json
{
  "server": {
    "name": "persona-server",
    "version": "1.0.0"
  },
  "storage": {
    "path": "/app/personas",
    "backup_path": "/app/backups"
  },
  "auto_generation": {
    "enabled": true,
    "confidence_threshold": 0.3
  }
}
```

### **Environment-Specific Builds**

```bash
# Production build
docker build --build-arg ENVIRONMENT=production -t mcp-persona-server:prod .

# Development build
docker build --build-arg ENVIRONMENT=development -t mcp-persona-server:dev .
```

### **Multi-Architecture Builds**

```bash
# Build for multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 -t mcp-persona-server:latest .
```

## Troubleshooting

### **Common Issues**

#### **1. Permission Denied**

```bash
# Fix script permissions
chmod +x scripts/docker-build.sh
chmod +x scripts/docker-run.sh
```

#### **2. Docker Not Running**

```bash
# Start Docker Desktop or Docker Engine
# On macOS: Open Docker Desktop
# On Linux: sudo systemctl start docker
```

#### **3. Port Already in Use**

```bash
# Check what's using the port
lsof -i :8000

# Stop conflicting containers
docker-compose down
```

#### **4. Volume Mount Issues**

```bash
# Create personas directory
mkdir -p ./personas

# Check volume permissions
ls -la ./personas
```

### **Debugging Commands**

```bash
# Check Docker images
docker images mcp-persona-server

# Check running containers
docker ps

# View container logs
docker logs mcp-persona-server

# Enter container shell
docker exec -it mcp-persona-server /bin/bash

# Check container resources
docker stats mcp-persona-server
```

### **Cleanup Commands**

```bash
# Remove all containers
docker rm -f $(docker ps -aq)

# Remove all images
docker rmi -f $(docker images -q)

# Remove volumes
docker volume prune

# Complete cleanup
docker system prune -a
```

## Performance Optimization

### **Image Size Optimization**

- Use multi-stage builds
- Remove unnecessary packages
- Use `.dockerignore` to exclude files

### **Runtime Optimization**

- Use volume mounts for persistent data
- Set appropriate resource limits
- Use health checks

### **Resource Limits**

```yaml
# In docker-compose.yml
services:
  mcp-persona-server:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
        reservations:
          memory: 256M
          cpus: "0.25"
```

## Security Considerations

### **Best Practices**

- **Non-root user**: Container runs as `mcp_user`
- **Read-only config**: Configuration mounted as read-only
- **Minimal base image**: Uses Python slim image
- **No unnecessary packages**: Removes build dependencies

### **Security Scanning**

```bash
# Scan for vulnerabilities
docker scan mcp-persona-server:latest

# Use security-focused base image
# Consider using distroless images for production
```

## Monitoring and Logging

### **Log Configuration**

```bash
# View real-time logs
docker logs -f mcp-persona-server

# View logs with timestamps
docker logs -t mcp-persona-server
```

### **Health Checks**

```yaml
# Add to docker-compose.yml
healthcheck:
  test: ["CMD", "python", "-c", "import mcp_persona_server"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Deployment Strategies

### **Local Development**

```bash
# Development with hot reloading
docker-compose --profile dev up

# With debugging
docker run -it --rm \
  -v $(pwd):/app \
  -p 8000:8000 \
  mcp-persona-server:dev
```

### **Production Deployment**

```bash
# Build production image
./scripts/docker-build.sh --tag production

# Deploy with persistent storage
./scripts/docker-run.sh --tag production
```

### **CI/CD Integration**

```yaml
# Example GitHub Actions workflow
name: Build and Deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: ./scripts/docker-build.sh --tag ${{ github.sha }}
      - name: Push to registry
        run: docker push mcp-persona-server:${{ github.sha }}
```

## Summary

The Docker setup provides:

✅ **Consistent environment** across different platforms
✅ **Easy deployment** with simple commands
✅ **Persistent data storage** for personas
✅ **Security best practices** with non-root user
✅ **Development and production** configurations
✅ **Integration ready** for Claude Desktop and other MCP clients

🎯 **Ready to containerize your MCP Persona Server!**
