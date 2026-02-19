#!/bin/bash
#
# Complete Docker Implementation Guide for marketing.tvoje.info
#
# This script demonstrates the full implementation process
# Run: bash scripts/implement-docker.sh

set -e

echo "🐳 Docker Implementation for marketing.tvoje.info"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${GREEN}✅${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠️${NC} $1"; }
print_error() { echo -e "${RED}❌${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ️${NC} $1"; }

# Phase 1: Pre-flight Checks
echo "Phase 1: Pre-flight Checks"
echo "--------------------------"

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker not installed"
    exit 1
fi
print_status "Docker is installed"

# Check Docker Compose
if ! docker-compose --version &> /dev/null; then
    print_error "Docker Compose not found"
    exit 1
fi
print_status "Docker Compose is available"

# Check environment
if [ ! -f .env ]; then
    print_warning ".env file not found"
    print_info "Creating from .env.example..."
    cp .env.example .env || print_warning "No .env.example found"
fi

# Phase 2: Build Configuration
echo ""
echo "Phase 2: Build Configuration"
echo "----------------------------"

# Build Astro site in Docker
print_info "Building Astro site in Docker container..."
docker-compose -f docker-compose.prod.yml --profile build run --rm astro-build

if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    print_status "Build successful - dist/ directory created"
else
    print_error "Build failed - dist/ directory empty"
    exit 1
fi

# Phase 3: Start Services
echo ""
echo "Phase 3: Start Services"
echo "-----------------------"

# Start Redis and MCP Gateway
print_info "Starting Redis and MCP Gateway..."
docker-compose -f docker-compose.prod.yml up -d redis mcp-gateway

# Wait for Redis
print_info "Waiting for Redis to be ready..."
sleep 5

if docker exec marketing-redis redis-cli -a marketing ping | grep -q "PONG"; then
    print_status "Redis is ready"
else
    print_error "Redis failed to start"
    exit 1
fi

# Phase 4: Verification
echo ""
echo "Phase 4: Verification"
echo "---------------------"

# Check running containers
print_info "Running containers:"
docker-compose -f docker-compose.prod.yml ps

# Test MCP Gateway
if curl -s http://localhost:3000/health | grep -q "ok"; then
    print_status "MCP Gateway is responding"
else
    print_warning "MCP Gateway health check not responding (may need more time)"
fi

# Show logs
print_info "Recent logs:"
docker-compose -f docker-compose.prod.yml logs --tail=20

# Phase 5: Next Steps
echo ""
echo "Phase 5: Next Steps"
echo "-------------------"
print_status "Docker implementation complete!"
echo ""
echo "To deploy to production (Server62):"
echo "  1. Copy dist/ to /var/www/portfolio/"
echo "  2. Reload Nginx: sudo nginx -s reload"
echo "  3. Verify: curl https://marketing.tvoje.info"
echo ""
echo "Useful commands:"
echo "  docker-compose -f docker-compose.prod.yml logs -f    # Follow logs"
echo "  docker-compose -f docker-compose.prod.yml down       # Stop services"
echo "  docker-compose -f docker-compose.prod.yml ps         # Check status"
echo ""
echo "Redis management:"
echo "  docker exec -it marketing-redis redis-cli -a marketing"
echo ""
print_status "Implementation guide complete!"
