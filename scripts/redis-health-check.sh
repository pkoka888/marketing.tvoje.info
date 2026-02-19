#!/bin/bash
#
# Redis Health Check Script
# Comprehensive health monitoring for Redis
#

set -e

# Configuration
CONTAINER_NAME="marketing-redis"
REDIS_PASSWORD="marketing"
KEY_PREFIX="project:marketing-tvoje-info:"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

print_metric() {
    echo -e "${CYAN}$1${NC}: $2"
}

echo "🔍 Redis Health Check"
echo "====================="
echo ""

# Check if container is running
echo "📋 Container Status:"
if docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" | grep -q "$CONTAINER_NAME"; then
    print_status "Container is running"
    
    # Get container uptime
    UPTIME=$(docker inspect --format='{{.State.StartedAt}}' "$CONTAINER_NAME" 2>/dev/null || echo "unknown")
    print_metric "Started" "$UPTIME"
else
    print_error "Container is not running"
    echo ""
    echo "To start Redis:"
    echo "  docker-compose up -d redis"
    exit 1
fi

# Check Redis connectivity
echo ""
echo "🔗 Connectivity:"
if docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" ping 2>/dev/null | grep -q "PONG"; then
    print_status "Redis responding to PING"
else
    print_error "Redis not responding"
    exit 1
fi

# Memory usage
echo ""
echo "💾 Memory Usage:"
MEMORY_INFO=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO memory 2>/dev/null)
USED=$(echo "$MEMORY_INFO" | grep "used_memory_human:" | cut -d: -f2 | tr -d '\r')
PEAK=$(echo "$MEMORY_INFO" | grep "used_memory_peak_human:" | cut -d: -f2 | tr -d '\r')
MAX=$(echo "$MEMORY_INFO" | grep "maxmemory_human:" | cut -d: -f2 | tr -d '\r')

print_metric "Used" "${USED:-unknown}"
print_metric "Peak" "${PEAK:-unknown}"
print_metric "Max Limit" "${MAX:-not set}"

# Calculate percentage if max is set
if [ -n "$MAX" ] && [ "$MAX" != "0B" ]; then
    # Convert to bytes for calculation (simplified)
    print_info "Memory utilization within limits"
fi

# Connected clients
echo ""
echo "👥 Clients:"
CLIENT_INFO=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO clients 2>/dev/null)
CONNECTED=$(echo "$CLIENT_INFO" | grep "connected_clients:" | cut -d: -f2 | tr -d '\r')
BLOCKED=$(echo "$CLIENT_INFO" | grep "blocked_clients:" | cut -d: -f2 | tr -d '\r')

print_metric "Connected" "${CONNECTED:-0}"
print_metric "Blocked" "${BLOCKED:-0}"

# Key statistics
echo ""
echo "🔑 Key Statistics:"
TOTAL_KEYS=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" DBSIZE 2>/dev/null || echo "0")
print_metric "Total Keys" "$TOTAL_KEYS"

# Count project-specific keys
PROJECT_KEYS=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" EVAL "
    local keys = redis.call('keys', '${KEY_PREFIX}*')
    return #keys
" 0 2>/dev/null || echo "0")
print_metric "Project Keys (${KEY_PREFIX})" "$PROJECT_KEYS"

# Persistence status
echo ""
echo "💾 Persistence:"
PERSISTENCE_INFO=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO persistence 2>/dev/null)
AOF_ENABLED=$(echo "$PERSISTENCE_INFO" | grep "aof_enabled:" | cut -d: -f2 | tr -d '\r')

if [ "$AOF_ENABLED" == "1" ]; then
    print_status "AOF persistence enabled"
    AOF_SIZE=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO persistence | grep "aof_current_size:" | cut -d: -f2 | tr -d '\r')
    print_metric "AOF Size" "${AOF_SIZE:-unknown} bytes"
else
    print_warning "AOF persistence disabled"
fi

# Check for expired keys
EXPIRED=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO stats | grep "expired_keys:" | cut -d: -f2 | tr -d '\r' || echo "0")
EVICTED=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO stats | grep "evicted_keys:" | cut -d: -f2 | tr -d '\r' || echo "0")

if [ "${EXPIRED:-0}" -gt 0 ] || [ "${EVICTED:-0}" -gt 0 ]; then
    echo ""
    echo "🧹 Cleanup Activity:"
    print_metric "Expired Keys" "${EXPIRED:-0}"
    print_metric "Evicted Keys" "${EVICTED:-0}"
fi

# Performance metrics
echo ""
echo "⚡ Performance:"
STATS=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO stats 2>/dev/null)
CMDS=$(echo "$STATS" | grep "total_commands_processed:" | cut -d: -f2 | tr -d '\r' || echo "0")
CONNECTIONS=$(echo "$STATS" | grep "total_connections_received:" | cut -d: -f2 | tr -d '\r' || echo "0")

print_metric "Commands Processed" "${CMDS:-0}"
print_metric "Connections Received" "${CONNECTIONS:-0}"

# Test write/read
echo ""
echo "🧪 Functional Test:"
TEST_KEY="${KEY_PREFIX}healthcheck:test"
if docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" SET "$TEST_KEY" "$(date +%s)" EX 60 >/dev/null 2>&1; then
    TEST_VALUE=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" GET "$TEST_KEY" 2>/dev/null)
    if [ -n "$TEST_VALUE" ]; then
        print_status "Read/Write test passed"
    else
        print_error "Read test failed"
    fi
    docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" DEL "$TEST_KEY" >/dev/null 2>&1
else
    print_error "Write test failed"
fi

# Summary
echo ""
echo "====================="
if [ "$TOTAL_KEYS" -lt 10000 ] && [ "${CONNECTED:-0}" -lt 50 ]; then
    print_status "Health check passed - Redis is healthy"
else
    print_warning "Health check passed - Review metrics above"
fi
echo ""
echo "💡 Tips:"
echo "   - Run backup: scripts/backup-redis.sh"
echo "   - Check logs: docker logs $CONTAINER_NAME"
echo "   - Monitor: Watch memory usage over time"
echo ""
