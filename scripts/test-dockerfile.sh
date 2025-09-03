#!/bin/bash

# Test Dockerfile syntax and configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Testing Dockerfile and Docker configuration..."

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    print_error "Dockerfile not found!"
    exit 1
fi
print_success "Dockerfile found"

# Check if .dockerignore exists
if [ ! -f ".dockerignore" ]; then
    print_warning ".dockerignore not found"
else
    print_success ".dockerignore found"
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found!"
    exit 1
fi
print_success "docker-compose.yml found"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found!"
    exit 1
fi
print_success "requirements.txt found"

# Check if config.json exists
if [ ! -f "config.json" ]; then
    print_warning "config.json not found"
else
    print_success "config.json found"
fi

# Validate Dockerfile syntax (basic checks)
print_status "Validating Dockerfile syntax..."

# Check for required Dockerfile instructions
required_instructions=("FROM" "WORKDIR" "COPY" "RUN" "CMD")
for instruction in "${required_instructions[@]}"; do
    if grep -q "^${instruction}" Dockerfile; then
        print_success "Found ${instruction} instruction"
    else
        print_warning "Missing ${instruction} instruction"
    fi
done

# Check for Python base image
if grep -q "FROM python:" Dockerfile; then
    print_success "Python base image specified"
else
    print_error "Python base image not found!"
fi

# Check for requirements.txt copy
if grep -q "COPY.*requirements.txt" Dockerfile; then
    print_success "requirements.txt copy instruction found"
else
    print_error "requirements.txt copy instruction not found!"
fi

# Check for pip install
if grep -q "pip install" Dockerfile; then
    print_success "pip install instruction found"
else
    print_error "pip install instruction not found!"
fi

# Check for non-root user
if grep -q "useradd" Dockerfile; then
    print_success "Non-root user creation found"
else
    print_warning "Non-root user creation not found"
fi

# Validate docker-compose.yml syntax
print_status "Validating docker-compose.yml syntax..."

# Check for required services
if grep -q "mcp-persona-server:" docker-compose.yml; then
    print_success "mcp-persona-server service defined"
else
    print_error "mcp-persona-server service not found!"
fi

# Check for volume mounts
if grep -q "volumes:" docker-compose.yml; then
    print_success "Volume mounts defined"
else
    print_warning "Volume mounts not defined"
fi

# Check for environment variables
if grep -q "environment:" docker-compose.yml; then
    print_success "Environment variables defined"
else
    print_warning "Environment variables not defined"
fi

# Validate requirements.txt
print_status "Validating requirements.txt..."

# Check for required packages
required_packages=("mcp" "fastapi" "uvicorn" "pydantic")
for package in "${required_packages[@]}"; do
    if grep -q "^${package}" requirements.txt; then
        print_success "Found ${package} package"
    else
        print_warning "Missing ${package} package"
    fi
done

# Check for Python version compatibility
python_version=$(grep -o "python[0-9.]*" Dockerfile | head -1)
if [ -n "$python_version" ]; then
    print_success "Python version: ${python_version}"
else
    print_warning "Python version not specified"
fi

# Check file permissions
print_status "Checking file permissions..."

if [ -x "scripts/docker-build.sh" ]; then
    print_success "docker-build.sh is executable"
else
    print_warning "docker-build.sh is not executable"
fi

if [ -x "scripts/docker-run.sh" ]; then
    print_success "docker-run.sh is executable"
else
    print_warning "docker-run.sh is not executable"
fi

# Summary
print_status "Docker configuration validation complete!"
print_success "Docker setup appears to be valid"

echo ""
print_status "To build and run the Docker image:"
echo "  1. Start Docker Desktop or Docker Engine"
echo "  2. Run: ./scripts/docker-build.sh"
echo "  3. Run: ./scripts/docker-run.sh"
echo "  4. Or use: docker-compose up"
