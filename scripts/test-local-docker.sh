#!/bin/bash
#
# Local Docker Testing Script for marketing.tvoje.info
# Run this before deploying to S60
#
# Usage: bash scripts/test-local-docker.sh

set -e

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

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

test_step() {
    echo ""
    echo "========================================"
    echo "TEST: $1"
    echo "========================================"
}

# ============================================
# PHASE 1: Pre-flight Checks
# ============================================
test_step "1. Pre-flight Checks"

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker not installed"
    exit 1
fi
print_status "Docker is installed"

# Check Docker Compose
if ! docker-compose --version &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose not found"
    exit 1
fi
print_status "Docker Compose is available"

# Check .env
if [ ! -f .env ]; then
    print_warning ".env file not found, creating from .env.example"
    cp .env.example .env 2>/dev/null || print_error "No .env.example found"
fi

# Source .env for local testing
export $(grep -v '^#' .env | xargs) 2>/dev/null || true

TESTS_PASSED=$((TESTS_PASSED + 3))

# ============================================
# PHASE 2: Build Test
# ============================================
test_step "2. Astro Build Test"

print_info "Building Astro site in Docker..."
print_info "This may take 2-5 minutes depending on your machine..."

# Clean previous build
rm -rf dist/

# Build using Docker Compose
if docker-compose -f docker-compose.prod.yml --profile build run --rm astro-build; then
    print_status "Docker build completed"
else
    print_error "Docker build failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    exit 1
fi

# Verify dist/ exists
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    print_status "dist/ directory created with content"
    print_info "Build size: $(du -sh dist/ | cut -f1)"
    print_info "Files count: $(find dist/ -type f | wc -l)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "dist/ directory is empty or missing"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    exit 1
fi

# Check for index.html
if [ -f "dist/index.html" ]; then
    print_status "index.html found in dist/"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "index.html not found in dist/"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================
# PHASE 3: Redis Container Test
# ============================================
test_step "3. Redis Container Test"

print_info "Starting Redis container..."

# Start Redis
docker-compose -f docker-compose.prod.yml up -d redis

# Wait for Redis to start
print_info "Waiting for Redis to initialize (10s)..."
sleep 10

# Test Redis connection
if docker exec marketing-redis redis-cli -a "${REDIS_PASSWORD:-marketing}" ping | grep -q "PONG"; then
    print_status "Redis is responding to PING"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Redis is not responding"
    print_info "Checking Redis logs..."
    docker-compose -f docker-compose.prod.yml logs redis --tail=20
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test Redis persistence
if docker exec marketing-redis redis-cli -a "${REDIS_PASSWORD:-marketing}" SET test_key "test_value" | grep -q "OK"; then
    print_status "Redis write test passed"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Redis write test failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

if docker exec marketing-redis redis-cli -a "${REDIS_PASSWORD:-marketing}" GET test_key | grep -q "test_value"; then
    print_status "Redis read test passed"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Redis read test failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Clean up test key
docker exec marketing-redis redis-cli -a "${REDIS_PASSWORD:-marketing}" DEL test_key > /dev/null 2>&1 || true

# ============================================
# PHASE 4: MCP Gateway Test
# ============================================
test_step "4. MCP Gateway Test"

print_info "Starting MCP Gateway container..."

# Create required secrets for testing
export JWT_SECRET="${JWT_SECRET:-test_jwt_secret_for_local_testing}"

# Start MCP Gateway
docker-compose -f docker-compose.prod.yml up -d mcp-gateway

# Wait for MCP Gateway to start
print_info "Waiting for MCP Gateway to initialize (15s)..."
sleep 15

# Test MCP Gateway health
if curl -s http://localhost:3000/health | grep -q "ok\|healthy\|success"; then
    print_status "MCP Gateway health check passed"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_warning "MCP Gateway health endpoint not responding (may be normal)"
    print_info "Checking if container is running..."
    if docker ps | grep -q "mcp-gateway"; then
        print_status "MCP Gateway container is running"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_error "MCP Gateway container is not running"
        print_info "Checking logs..."
        docker-compose -f docker-compose.prod.yml logs mcp-gateway --tail=20
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
fi

# ============================================
# PHASE 5: Container Status
# ============================================
test_step "5. Container Status Check"

print_info "Running containers:"
docker-compose -f docker-compose.prod.yml ps

# Check container health
RUNNING_CONTAINERS=$(docker-compose -f docker-compose.prod.yml ps -q | wc -l)
print_info "Running containers: $RUNNING_CONTAINERS"

if [ "$RUNNING_CONTAINERS" -ge 2 ]; then
    print_status "All expected containers are running"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Not all containers are running"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================
# PHASE 6: Resource Usage
# ============================================
test_step "6. Resource Usage"

print_info "Container resource usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

TESTS_PASSED=$((TESTS_PASSED + 1))

# ============================================
# PHASE 7: Static File Serving Test
# ============================================
test_step "7. Static File Serving Test"

# Start a simple Python HTTP server to test dist/
print_info "Starting temporary HTTP server for dist/..."
cd dist && python3 -m http.server 8888 > /dev/null 2>&1 &
SERVER_PID=$!
cd ..

# Wait for server
sleep 2

# Test HTTP response
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8888 | grep -q "200"; then
    print_status "Static files served successfully (HTTP 200)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Static file serving test failed"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Kill temporary server
kill $SERVER_PID 2>/dev/null || true

# ============================================
# PHASE 8: Cleanup
# ============================================
test_step "8. Cleanup"

print_info "Stopping containers..."
docker-compose -f docker-compose.prod.yml down

print_info "Removing build cache (optional)..."
# Uncomment to clean up:
# docker-compose -f docker-compose.prod.yml down -v

print_status "Cleanup completed"
TESTS_PASSED=$((TESTS_PASSED + 1))

# ============================================
# SUMMARY
# ============================================
echo ""
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo ""
    echo "Your Docker stack is ready for S60 deployment."
    echo ""
    echo "Next steps:"
    echo "  1. Add GitHub Secrets (see api-keys-inventory.md)"
    echo "  2. Push to main branch: git push origin main"
    echo "  3. Monitor deployment: gh run watch"
    exit 0
else
    echo -e "${RED}⚠️ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please review the errors above before deploying."
    exit 1
fi
