#!/bin/bash

# Docker build script for MCP Persona Server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
IMAGE_NAME="mcp-persona-server"
TAG="latest"
BUILD_TYPE="production"

# Function to print colored output
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

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --tag)
            TAG="$2"
            shift 2
            ;;
        --dev)
            BUILD_TYPE="development"
            TAG="dev"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --tag TAG     Specify image tag (default: latest)"
            echo "  --dev         Build development image"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_status "Building MCP Persona Server Docker image..."
print_status "Image: ${IMAGE_NAME}:${TAG}"
print_status "Build type: ${BUILD_TYPE}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the image
print_status "Building Docker image..."
if docker build -t "${IMAGE_NAME}:${TAG}" .; then
    print_success "Docker image built successfully!"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Show image info
print_status "Image details:"
docker images "${IMAGE_NAME}:${TAG}"

print_success "Build completed! You can now run the container with:"
echo "  docker run -it --rm ${IMAGE_NAME}:${TAG}"
echo "  or"
echo "  docker-compose up"
