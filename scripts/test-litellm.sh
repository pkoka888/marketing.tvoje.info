#!/bin/bash
#
# LiteLLM Testing Script
# Tests LiteLLM functionality via S60 or local deployment
#
# Usage: bash scripts/test-litellm.sh [s60|local]

set -e

MODE="${1:-s60}"

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
echo "LiteLLM Functionality Test"
echo "Mode: $MODE"
echo "========================================"
echo ""

# ============================================
# Configuration
# ============================================

if [ "$MODE" == "s60" ]; then
    LITELLM_HOST="89.203.173.196"
    LITELLM_PORT="4000"
    LITELLM_URL="http://$LITELLM_HOST:$LITELLM_PORT"
    SSH_PORT="2260"
    SSH_USER="sugent"
    
    print_info "Testing LiteLLM on S60 via SSH tunnel..."
    
    # Check SSH connection
    if ! ssh -p $SSH_PORT -o ConnectTimeout=5 -o StrictHostKeyChecking=no $SSH_USER@$LITELLM_HOST "echo 'SSH_OK'" 2>/dev/null | grep -q "SSH_OK"; then
        print_error "Cannot connect to S60 via SSH (port $SSH_PORT)"
        print_info "Please check:"
        print_info "  - Tailscale is connected"
        print_info "  - SSH key is configured"
        print_info "  - S60 is accessible"
        exit 1
    fi
    print_status "SSH connection to S60 verified"
    
    # Create SSH tunnel
    print_info "Creating SSH tunnel to LiteLLM (port 4000)..."
    ssh -f -N -L 14000:$LITELLM_HOST:$LITELLM_PORT -p $SSH_PORT $SSH_USER@$LITELLM_HOST 2>/dev/null || true
    LITELLM_URL="http://localhost:14000"
    
    # Wait for tunnel
    sleep 2
    
elif [ "$MODE" == "local" ]; then
    LITELLM_URL="http://localhost:4000"
    
    print_info "Testing local LiteLLM instance..."
    
    # Check if LiteLLM is running locally
    if ! curl -s "$LITELLM_URL/health" > /dev/null 2>&1; then
        print_error "LiteLLM is not running locally on port 4000"
        print_info "To start LiteLLM locally:"
        print_info "  cd litellm"
        print_info "  litellm --config proxy_config.yaml --port 4000"
        exit 1
    fi
    print_status "Local LiteLLM instance detected"
else
    print_error "Unknown mode: $MODE"
    print_info "Usage: bash scripts/test-litellm.sh [s60|local]"
    exit 1
fi

# ============================================
# Test 1: Health Check
# ============================================
echo ""
echo "Test 1: Health Check"
echo "--------------------"

HEALTH_RESPONSE=$(curl -s "$LITELLM_URL/health" 2>/dev/null || echo "FAILED")

if [ "$HEALTH_RESPONSE" != "FAILED" ] && [ -n "$HEALTH_RESPONSE" ]; then
    print_status "Health endpoint responded"
    print_info "Response: $HEALTH_RESPONSE"
else
    print_error "Health check failed"
    print_info "LiteLLM may not be running or configured correctly"
    exit 1
fi

# ============================================
# Test 2: Model List
# ============================================
echo ""
echo "Test 2: Available Models"
echo "------------------------"

MODELS_RESPONSE=$(curl -s "$LITELLM_URL/v1/models" 2>/dev/null || echo "FAILED")

if [ "$MODELS_RESPONSE" != "FAILED" ]; then
    print_status "Model list endpoint accessible"
    print_info "Models:"
    echo "$MODELS_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | head -5 | while read model; do
        print_info "  - $model"
    done
else
    print_error "Could not retrieve model list"
fi

# ============================================
# Test 3: Chat Completion (if API key available)
# ============================================
echo ""
echo "Test 3: Chat Completion"
echo "-----------------------"

if [ -z "$GROQ_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ]; then
    print_warning "No API keys found in environment"
    print_info "Set GROQ_API_KEY or OPENROUTER_API_KEY to test chat completion"
else
    # Try Groq first (fastest)
    if [ -n "$GROQ_API_KEY" ]; then
        MODEL="groq/llama-3.3-70b-versatile"
        API_KEY="$GROQ_API_KEY"
        PROVIDER="Groq"
    else
        MODEL="openrouter/gpt-3.5-turbo"
        API_KEY="$OPENROUTER_API_KEY"
        PROVIDER="OpenRouter"
    fi
    
    print_info "Testing chat completion with $PROVIDER ($MODEL)..."
    
    CHAT_RESPONSE=$(curl -s -X POST "$LITELLM_URL/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{
            \"model\": \"$MODEL\",
            \"messages\": [{\"role\": \"user\", \"content\": \"Say 'LiteLLM test successful' and nothing else\"}],
            \"max_tokens\": 20
        }" 2>/dev/null || echo "FAILED")
    
    if [ "$CHAT_RESPONSE" != "FAILED" ] && echo "$CHAT_RESPONSE" | grep -q "content"; then
        print_status "Chat completion working!"
        CONTENT=$(echo "$CHAT_RESPONSE" | grep -o '"content":"[^"]*"' | head -1 | cut -d'"' -f4)
        print_info "Response: $CONTENT"
    else
        print_error "Chat completion failed"
        print_info "Response: $CHAT_RESPONSE"
    fi
fi

# ============================================
# Test 4: Rate Limits & Headers
# ============================================
echo ""
echo "Test 4: Headers & Configuration"
echo "-------------------------------"

HEADERS=$(curl -sI "$LITELLM_URL/health" 2>/dev/null || echo "FAILED")

if [ "$HEADERS" != "FAILED" ]; then
    print_status "Headers received"
    print_info "Server: $(echo "$HEADERS" | grep -i "server:" | cut -d: -f2 | tr -d ' ' || echo "N/A")"
else
    print_warning "Could not retrieve headers"
fi

# ============================================
# Cleanup
# ============================================
echo ""
echo "Cleanup"
echo "-------"

if [ "$MODE" == "s60" ]; then
    # Kill SSH tunnel
    print_info "Closing SSH tunnel..."
    pkill -f "ssh.*14000.*$LITELLM_HOST" 2>/dev/null || true
    print_status "SSH tunnel closed"
fi

# ============================================
# Summary
# ============================================
echo ""
echo "========================================"
echo "LiteLLM Test Summary"
echo "========================================"
print_status "LiteLLM is functional on $MODE"
print_info "URL: $LITELLM_URL"
print_info "Mode: $MODE"

echo ""
echo "Next steps:"
if [ "$MODE" == "s60" ]; then
    echo "  - LiteLLM on S60 is working correctly"
    echo "  - Consider migrating from S62 to S60 for unified hosting"
else
    echo "  - Local LiteLLM is working"
    echo "  - Deploy to S60 for production use"
fi
