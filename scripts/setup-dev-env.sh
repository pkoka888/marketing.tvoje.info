#!/bin/bash
#
# Local Development Environment Setup
# Sets up the complete local dev stack
#
# Usage: bash scripts/setup-dev-env.sh

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

echo "========================================"
echo "LOCAL DEVELOPMENT SETUP"
echo "========================================"
echo ""

# ============================================
# Step 1: Check Prerequisites
# ============================================
print_info "Step 1: Checking Prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi

print_status "All prerequisites met"

# ============================================
# Step 2: Setup .env file
# ============================================
print_info "Step 2: Setting up environment..."

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        print_status ".env file created from .env.example"
        print_warning "Please edit .env and add your API keys"
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_status ".env file already exists"
fi

# ============================================
# Step 3: Install Node dependencies
# ============================================
print_info "Step 3: Installing Node dependencies..."

if [ ! -d node_modules ]; then
    npm install
    print_status "Dependencies installed"
else
    print_status "Dependencies already installed"
fi

# ============================================
# Step 4: Start development services
# ============================================
print_info "Step 4: Starting development services..."

docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
docker-compose -f docker-compose.dev.yml up -d redis-dev mcp-gateway-dev

print_info "Waiting for services to start..."
sleep 10

# Check Redis
if docker exec marketing-redis-dev redis-cli ping | grep -q "PONG"; then
    print_status "Redis is running on port 6379"
else
    print_warning "Redis may still be starting..."
fi

# Check MCP Gateway
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    print_status "MCP Gateway is running on port 3000"
else
    print_warning "MCP Gateway may still be starting..."
fi

# ============================================
# Step 5: Optional - Start LiteLLM
# ============================================
print_info "Step 5: Checking LiteLLM..."

if [ -n "$GROQ_API_KEY" ] || [ -n "$OPENROUTER_API_KEY" ]; then
    print_info "API keys found. LiteLLM can be started with:"
    print_info "  docker-compose -f docker-compose.dev.yml --profile litellm up -d litellm-dev"
else
    print_warning "No API keys found. LiteLLM will not be started."
    print_info "Add GROQ_API_KEY or OPENROUTER_API_KEY to .env to use LiteLLM"
fi

# ============================================
# Step 6: Setup Git hooks
# ============================================
print_info "Step 6: Setting up Git hooks..."

if [ -d .git ]; then
    cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash
# Pre-commit hook for validation

echo "Running pre-commit checks..."

# Check for secrets
if grep -r "sk-" .env 2>/dev/null | grep -v ".env.example" | grep -v "^#"; then
    echo "⚠️  Warning: Potential secrets in .env"
fi

# Run quick validation if script exists
if [ -f scripts/quick-docker-validate.sh ]; then
    bash scripts/quick-docker-validate.sh
fi

echo "Pre-commit checks complete"
HOOK
    chmod +x .git/hooks/pre-commit
    print_status "Pre-commit hook installed"
else
    print_warning "Not a git repository, skipping hooks"
fi

# ============================================
# Summary
# ============================================
echo ""
echo "========================================"
echo "SETUP COMPLETE!"
echo "========================================"
echo ""
print_status "Development environment is ready"
echo ""
echo "Services running:"
echo "  - Redis:        localhost:6379"
echo "  - MCP Gateway:  http://localhost:3000"
echo ""
echo "Useful commands:"
echo "  npm run dev              # Start Astro dev server"
echo "  npm run build            # Build for production"
echo "  npm run test             # Run tests"
echo ""
echo "Docker commands:"
echo "  docker-compose -f docker-compose.dev.yml logs -f"
echo "  docker-compose -f docker-compose.dev.yml down"
echo ""
echo "To start LiteLLM:"
echo "  docker-compose -f docker-compose.dev.yml --profile litellm up -d litellm-dev"
echo ""
