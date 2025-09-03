#!/bin/bash

# Docker run script for MCP Persona Server

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
CONTAINER_NAME="mcp-persona-server"
PERSISTENT_DATA=true

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
        --name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        --no-persist)
            PERSISTENT_DATA=false
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --tag TAG         Specify image tag (default: latest)"
            echo "  --name NAME       Specify container name (default: mcp-persona-server)"
            echo "  --no-persist      Don't persist data (use temporary storage)"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_status "Running MCP Persona Server in Docker..."
print_status "Image: ${IMAGE_NAME}:${TAG}"
print_status "Container: ${CONTAINER_NAME}"
print_status "Persistent data: ${PERSISTENT_DATA}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if image exists
if ! docker images | grep -q "${IMAGE_NAME}.*${TAG}"; then
    print_warning "Image ${IMAGE_NAME}:${TAG} not found. Building it first..."
    ./scripts/docker-build.sh --tag "${TAG}"
fi

# Create personas directory if it doesn't exist
if [ "$PERSISTENT_DATA" = true ]; then
    mkdir -p ./personas
    print_status "Using persistent storage in ./personas"
fi

# Stop and remove existing container if it exists
if docker ps -a | grep -q "${CONTAINER_NAME}"; then
    print_status "Stopping existing container..."
    docker stop "${CONTAINER_NAME}" > /dev/null 2>&1 || true
    docker rm "${CONTAINER_NAME}" > /dev/null 2>&1 || true
fi

# Run the container
print_status "Starting container..."

if [ "$PERSISTENT_DATA" = true ]; then
    # Run with persistent storage
    docker run -it --rm \
        --name "${CONTAINER_NAME}" \
        -v "$(pwd)/personas:/app/personas" \
        -v "$(pwd)/config.json:/app/config.json:ro" \
        -e PERSONA_STORAGE_PATH=/app/personas \
        -e PYTHONPATH=/app \
        -e PYTHONUNBUFFERED=1 \
        "${IMAGE_NAME}:${TAG}"
else
    # Run with temporary storage
    docker run -it --rm \
        --name "${CONTAINER_NAME}" \
        -e PERSONA_STORAGE_PATH=/app/personas \
        -e PYTHONPATH=/app \
        -e PYTHONUNBUFFERED=1 \
        "${IMAGE_NAME}:${TAG}"
fi

print_success "Container stopped."
