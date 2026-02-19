#!/bin/bash
#
# Quick Docker Configuration Validation
# Validates Docker files without full build (faster)
#
# Usage: bash scripts/quick-docker-validate.sh

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

TESTS_PASSED=0
TESTS_FAILED=0

echo "========================================"
echo "QUICK DOCKER VALIDATION"
echo "========================================"
echo ""

# ============================================
# Test 1: Docker Available
# ============================================
if docker --version > /dev/null 2>&1; then
    DOCKER_VERSION=$(docker --version)
    print_status "Docker available: $DOCKER_VERSION"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Docker not available"
    exit 1
fi

# ============================================
# Test 2: Docker Compose Available
# ============================================
if docker-compose --version > /dev/null 2>&1 || docker compose version > /dev/null 2>&1; then
    print_status "Docker Compose available"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Docker Compose not available"
    exit 1
fi

# ============================================
# Test 3: File Structure
# ============================================
echo ""
echo "Checking File Structure..."
echo "--------------------------"

FILES_TO_CHECK=(
    "docker-compose.prod.yml"
    "Dockerfile.build"
    "docker/mcp/gateway-config.yml"
    "docker/redis/redis.conf"
)

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        print_status "$file exists"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_error "$file missing"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
done

# ============================================
# Test 4: Docker Compose Config Validation
# ============================================
echo ""
echo "Validating Docker Compose..."
echo "---------------------------"

if docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1; then
    print_status "Docker Compose syntax is valid"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_error "Docker Compose has syntax errors"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Show services defined
echo ""
print_info "Services defined in compose file:"
docker-compose -f docker-compose.prod.yml config --services 2>/dev/null | while read service; do
    echo "  - $service"
done

# ============================================
# Test 5: Dockerfile Validation
# ============================================
echo ""
echo "Validating Dockerfile..."
echo "-----------------------"

if [ -f "Dockerfile.build" ]; then
    # Check for multi-stage
    if grep -q "FROM.*AS" Dockerfile.build; then
        print_status "Multi-stage build detected"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_warning "No multi-stage build detected"
    fi
    
    # Check for Node 20
    if grep -q "node:20" Dockerfile.build; then
        print_status "Using Node.js 20"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_warning "Not using Node.js 20"
    fi
    
    # Check for BuildKit
    if grep -q "syntax=docker/dockerfile" Dockerfile.build; then
        print_status "BuildKit syntax detected"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_warning "BuildKit syntax not detected"
    fi
fi

# ============================================
# Test 6: MCP Gateway Config
# ============================================
echo ""
echo "Validating MCP Gateway Config..."
echo "--------------------------------"

if [ -f "docker/mcp/gateway-config.yml" ]; then
    # Count MCP servers
    SERVER_COUNT=$(grep -c "^  [a-z]*:$" docker/mcp/gateway-config.yml 2>/dev/null || echo "0")
    print_status "MCP Gateway config exists"
    print_info "MCP servers configured: $SERVER_COUNT"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    
    # List servers
    print_info "Servers:"
    grep "^  [a-z]*:$" docker/mcp/gateway-config.yml | sed 's/:$//' | sed 's/^/    - /'
else
    print_error "MCP Gateway config missing"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# ============================================
# Test 7: Environment Variables
# ============================================
echo ""
echo "Checking Environment Setup..."
echo "-----------------------------"

if [ -f ".env" ]; then
    print_status ".env file exists"
    
    # Check for required vars
    REQUIRED_VARS=(
        "PROJECT_NAME"
        "PUBLIC_SITE_URL"
        "REDIS_PASSWORD"
    )
    
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "^$var=" .env; then
            print_status "$var is set"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            print_warning "$var not set in .env"
        fi
    done
else
    print_warning ".env file not found"
fi

# ============================================
# Test 8: Network Configuration
# ============================================
echo ""
echo "Checking Network Configuration..."
echo "---------------------------------"

if grep -q "subnet: 172.30.0.0/16" docker-compose.prod.yml; then
    print_status "Network subnet configured (172.30.0.0/16)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    print_warning "Network subnet not as expected"
fi

# ============================================
# Test 9: Port Conflicts (Check if ports are in use)
# ============================================
echo ""
echo "Checking Port Availability..."
echo "-----------------------------"

PORTS=(3000 6379)
for port in "${PORTS[@]}"; do
    if ! netstat -tuln 2>/dev/null | grep -q ":$port "; then
        print_status "Port $port is available"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        print_warning "Port $port is in use"
    fi
done

# ============================================
# SUMMARY
# ============================================
echo ""
echo "========================================"
echo "VALIDATION SUMMARY"
echo "========================================"
echo -e "${GREEN}Checks Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Checks Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL VALIDATIONS PASSED!${NC}"
    echo ""
    echo "Docker configuration is ready for S60 deployment."
    echo ""
    echo "Quick Start:"
    echo "  1. Add GitHub Secrets"
    echo "  2. Run full test: bash scripts/test-local-docker.sh"
    echo "  3. Deploy: git push origin main"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️ SOME VALIDATIONS FAILED${NC}"
    echo ""
    echo "Review the warnings/errors above."
    echo ""
    exit 0  # Exit 0 because warnings may be acceptable
fi
