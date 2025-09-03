# Docker Quick Reference

## 🚀 Quick Start

```bash
# Test Docker setup (no Docker required)
make docker-test

# Build and run (requires Docker)
make docker-build
make docker-run

# Or use Docker Compose
docker-compose up
```

## 📋 Essential Commands

### **Building**

```bash
# Build image
./scripts/docker-build.sh
docker build -t mcp-persona-server:latest .

# Build with tag
./scripts/docker-build.sh --tag v1.0.0
docker build -t mcp-persona-server:v1.0.0 .
```

### **Running**

```bash
# Run with persistent storage
./scripts/docker-run.sh
docker run -it --rm -v $(pwd)/personas:/app/personas mcp-persona-server:latest

# Run with temporary storage
./scripts/docker-run.sh --no-persist
docker run -it --rm mcp-persona-server:latest
```

### **Docker Compose**

```bash
# Start service
docker-compose up

# Start in background
docker-compose up -d

# Stop service
docker-compose down

# View logs
docker-compose logs -f
```

## 🔧 Configuration

### **Environment Variables**

```bash
PERSONA_STORAGE_PATH=/app/personas
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### **Volume Mounts**

```bash
# Persistent personas
-v $(pwd)/personas:/app/personas

# Configuration
-v $(pwd)/config.json:/app/config.json:ro
```

## 🐛 Troubleshooting

### **Common Issues**

```bash
# Check Docker status
docker info

# Check images
docker images mcp-persona-server

# Check containers
docker ps -a

# View logs
docker logs mcp-persona-server

# Enter container
docker exec -it mcp-persona-server /bin/bash
```

### **Cleanup**

```bash
# Remove containers
docker rm -f $(docker ps -aq)

# Remove images
docker rmi -f $(docker images -q)

# Full cleanup
docker system prune -a
```

## 🔗 Integration

### **Claude Desktop**

```json
{
  "mcpServers": {
    "persona-server": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "/path/to/personas:/app/personas", "mcp-persona-server:latest"]
    }
  }
}
```

### **Docker Compose Integration**

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

## 📊 Monitoring

### **Resource Usage**

```bash
# Container stats
docker stats mcp-persona-server

# Resource limits
docker run --memory=512m --cpus=0.5 mcp-persona-server:latest
```

### **Health Checks**

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import mcp_persona_server"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🛡️ Security

### **Best Practices**

- ✅ Non-root user (`mcp_user`)
- ✅ Read-only configuration
- ✅ Minimal base image
- ✅ No unnecessary packages

### **Security Scanning**

```bash
# Scan for vulnerabilities
docker scan mcp-persona-server:latest
```

## 📈 Performance

### **Optimization Tips**

- Use volume mounts for persistent data
- Set appropriate resource limits
- Use multi-stage builds
- Exclude unnecessary files with `.dockerignore`

### **Resource Limits Example**

```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: "0.5"
    reservations:
      memory: 256M
      cpus: "0.25"
```

## 🔄 CI/CD

### **GitHub Actions Example**

```yaml
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

## 📝 Makefile Commands

```bash
# Docker operations
make docker-build
make docker-run
make docker-test
make docker-clean

# Docker Compose
make compose-up
make compose-down
make compose-logs

# Quick start
make quick-start

# Production
make prod-build
make prod-run
```

## 🎯 Key Features

- ✅ **Persistent Storage**: Personas saved to host filesystem
- ✅ **Security**: Non-root user and minimal attack surface
- ✅ **Performance**: Optimized Python 3.11 slim image
- ✅ **Flexibility**: Configurable via environment variables
- ✅ **Integration**: Ready for Claude Desktop and MCP clients
- ✅ **Monitoring**: Built-in logging and health checks

---

**Ready to containerize your MCP Persona Server! 🐳**
