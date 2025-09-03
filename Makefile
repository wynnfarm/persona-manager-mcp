# Makefile for MCP Persona Server

.PHONY: help build run test clean docker-build docker-run docker-test docker-clean

# Default target
help:
	@echo "MCP Persona Server - Available Commands:"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build    Build the Docker image"
	@echo "  docker-run      Run the Docker container"
	@echo "  docker-test     Test Docker configuration"
	@echo "  docker-clean    Clean up Docker resources"
	@echo ""
	@echo "Development Commands:"
	@echo "  install         Install Python dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Run linting"
	@echo "  clean           Clean up Python artifacts"
	@echo ""
	@echo "Utility Commands:"
	@echo "  status          Show project status"
	@echo "  docs            Generate documentation"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	@./scripts/docker-build.sh

docker-run:
	@echo "Running Docker container..."
	@./scripts/docker-run.sh

docker-test:
	@echo "Testing Docker configuration..."
	@./scripts/test-dockerfile.sh

docker-clean:
	@echo "Cleaning up Docker resources..."
	@docker system prune -f
	@docker image prune -f
	@docker container prune -f

# Development commands
install:
	@echo "Installing Python dependencies..."
	@pip install -r requirements.txt

test:
	@echo "Running tests..."
	@python -m pytest tests/ -v

lint:
	@echo "Running linting..."
	@flake8 mcp_persona_server/ --max-line-length=100
	@black --check mcp_persona_server/

clean:
	@echo "Cleaning up Python artifacts..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Utility commands
status:
	@./scripts/status.sh

quick-status:
	@echo "🎯 Current Goal: Deploy MCP Persona Server in Docker"
	@echo "🔧 Issue: Server initialization error (NotificationOptions)"
	@echo "📋 Next: Fix server.py → rebuild → test"

docs:
	@echo "Generating documentation..."
	@mkdir -p docs
	@echo "# MCP Persona Server Documentation" > docs/README.md
	@echo "" >> docs/README.md
	@echo "Generated on: $(shell date)" >> docs/README.md
	@echo "" >> docs/README.md
	@echo "## Project Structure" >> docs/README.md
	@echo "" >> docs/README.md
	@find . -name "*.py" -not -path "./venv/*" -not -path "./env/*" | head -10 | sed 's/^/- /' >> docs/README.md

# Docker Compose commands
compose-up:
	@echo "Starting services with Docker Compose..."
	@docker-compose up

compose-down:
	@echo "Stopping services..."
	@docker-compose down

compose-logs:
	@echo "Showing logs..."
	@docker-compose logs -f

# Quick start commands
quick-start: docker-build docker-run

dev-setup: install test lint

# Production commands
prod-build:
	@echo "Building production image..."
	@./scripts/docker-build.sh --tag production

prod-run:
	@echo "Running production container..."
	@./scripts/docker-run.sh --tag production

# Backup and restore
backup:
	@echo "Creating backup..."
	@mkdir -p backups
	@cp -r personas/ backups/personas-$(shell date +%Y%m%d-%H%M%S)/

restore:
	@echo "Available backups:"
	@ls -la backups/ 2>/dev/null || echo "No backups found"

# Context Management
context-status:
	@python context_check.py

context-init:
	@python -c "from context_manager.core import ContextManager; cm = ContextManager('$(shell basename $(PWD))'); cm.set_current_goal('Initialize project context'); print('✅ Context initialized')"

context-summary:
	@python -c "from context_manager.utils import quick_status_check; print(quick_status_check())"

context-update:
	@echo "Updating context..."
	@python -c "from context_manager.core import ContextManager; cm = ContextManager('$(shell basename $(PWD))'); print('✅ Context updated')"
