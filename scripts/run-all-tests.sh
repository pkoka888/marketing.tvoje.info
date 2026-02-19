#!/bin/bash
#
# Master Test Runner
# Runs all local tests in sequence
#
# Usage: bash scripts/run-all-tests.sh

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

OVERALL_PASSED=0
OVERALL_FAILED=0

# Header
echo "========================================"
echo "COMPREHENSIVE LOCAL TEST SUITE"
echo "marketing.tvoje.info"
echo "========================================"
echo ""
print_info "This will run all tests locally before S60 deployment"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Tests cancelled by user"
    exit 0
fi

# ============================================
# Test 1: Docker Local Test
# ============================================
echo ""
echo "========================================"
echo "TEST SUITE 1/3: Docker Stack"
echo "========================================"

if bash scripts/test-local-docker.sh; then
    print_status "Docker tests completed"
    OVERALL_PASSED=$((OVERALL_PASSED + 1))
else
    print_error "Docker tests failed"
    OVERALL_FAILED=$((OVERALL_FAILED + 1))
fi

# ============================================
# Test 2: MCP Servers
# ============================================
echo ""
echo "========================================"
echo "TEST SUITE 2/3: MCP Servers"
echo "========================================"

if bash scripts/test-mcp-servers.sh; then
    print_status "MCP server tests completed"
    OVERALL_PASSED=$((OVERALL_PASSED + 1))
else
    print_error "MCP server tests failed"
    OVERALL_FAILED=$((OVERALL_FAILED + 1))
fi

# ============================================
# Test 3: LiteLLM (Optional)
# ============================================
echo ""
echo "========================================"
echo "TEST SUITE 3/3: LiteLLM (Optional)"
echo "========================================"

if [ -n "$GROQ_API_KEY" ] || [ -n "$OPENROUTER_API_KEY" ]; then
    print_info "API keys found, testing LiteLLM..."
    
    # Check if S60 is accessible
    if ssh -p 2260 -o ConnectTimeout=3 -o StrictHostKeyChecking=no sugent@89.203.173.196 "echo OK" 2>/dev/null | grep -q "OK"; then
        print_info "S60 accessible, testing remote LiteLLM..."
        if bash scripts/test-litellm.sh s60; then
            print_status "LiteLLM (S60) tests completed"
            OVERALL_PASSED=$((OVERALL_PASSED + 1))
        else
            print_warning "LiteLLM (S60) tests had issues"
            # Don't count as failure - S60 may not have LiteLLM yet
        fi
    else
        print_warning "S60 not accessible, skipping remote LiteLLM test"
    fi
    
    # Check if local LiteLLM is running
    if curl -s http://localhost:4000/health > /dev/null 2>&1; then
        print_info "Local LiteLLM detected, testing..."
        if bash scripts/test-litellm.sh local; then
            print_status "LiteLLM (local) tests completed"
            OVERALL_PASSED=$((OVERALL_PASSED + 1))
        else
            print_warning "LiteLLM (local) tests had issues"
        fi
    else
        print_info "Local LiteLLM not running, skipping local test"
    fi
else
    print_warning "No API keys found, skipping LiteLLM tests"
    print_info "Set GROQ_API_KEY or OPENROUTER_API_KEY to test LiteLLM"
fi

# ============================================
# Final Summary
# ============================================
echo ""
echo "========================================"
echo "OVERALL TEST SUMMARY"
echo "========================================"
echo -e "${GREEN}Test Suites Passed: $OVERALL_PASSED${NC}"
echo -e "${RED}Test Suites Failed: $OVERALL_FAILED${NC}"
echo ""

if [ $OVERALL_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo ""
    echo "========================================"
    echo "READY FOR S60 DEPLOYMENT"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "  1. Add GitHub Secrets (see api-keys-inventory.md)"
    echo "  2. Commit these test scripts:"
    echo "     git add scripts/test-*.sh scripts/run-all-tests.sh"
    echo "     git commit -m 'test: add comprehensive test suite'"
    echo "  3. Push to main:"
    echo "     git push origin main"
    echo "  4. Monitor deployment:"
    echo "     gh run watch"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please review the errors above before deploying."
    echo "Fix the issues and run: bash scripts/run-all-tests.sh"
    exit 1
fi
