#!/bin/bash
#
# Cache Cleanup Script for Git Bash
# Cleans various caches to free space and fix issues
#

set -e

echo "🧹 Cache Cleanup Script"
echo "======================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# 1. Clean npm cache
echo "📦 Cleaning npm cache..."
if npm cache clean --force 2>/dev/null; then
    print_status "npm cache cleaned"
else
    print_warning "npm cache clean failed or not needed"
fi

# 2. Clean node_modules/.cache
echo ""
echo "🗑️  Cleaning node_modules/.cache..."
if [ -d "node_modules/.cache" ]; then
    rm -rf node_modules/.cache
    print_status "node_modules/.cache removed"
else
    print_warning "node_modules/.cache not found"
fi

# 3. Clean Astro cache
echo ""
echo "🚀 Cleaning Astro cache..."
if [ -d ".astro" ]; then
    rm -rf .astro
    print_status ".astro cache removed"
else
    print_warning ".astro cache not found"
fi

# 4. Clean dist/build directories
echo ""
echo "🏗️  Cleaning build directories..."
if [ -d "dist" ]; then
    rm -rf dist
    print_status "dist/ removed"
else
    print_warning "dist/ not found"
fi

# 5. Clean IDE caches
echo ""
echo "💻 Cleaning IDE caches..."

# VSCode
if [ -d ".vscode/.cache" ]; then
    rm -rf .vscode/.cache
    print_status ".vscode/.cache removed"
fi

# Clean temporary files
echo ""
echo "🧹 Cleaning temporary files..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
print_status "Temporary files cleaned"

# 6. Docker cleanup (if docker is available)
echo ""
echo "🐳 Checking Docker cleanup..."
if command -v docker &> /dev/null; then
    echo "   Docker system prune -a --volumes (manual confirmation required)"
    echo "   Run 'docker system prune -a --volumes' to clean Docker"
else
    print_warning "Docker not available"
fi

# Summary
echo ""
echo "======================="
echo "✅ Cache cleanup complete!"
echo ""
echo "💡 Tips:"
echo "   - Run 'npm ci' to reinstall dependencies if needed"
echo "   - Run 'npm run build' to rebuild the project"
echo ""
