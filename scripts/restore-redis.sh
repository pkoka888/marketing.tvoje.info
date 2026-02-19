#!/bin/bash
#
# Redis Restore Script
# Restores Redis from backup file
#

set -e

# Configuration
CONTAINER_NAME="marketing-redis"
REDIS_PASSWORD="marketing"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

# Help
if [ -z "$1" ] || [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "🔄 Redis Restore Script"
    echo "======================="
    echo ""
    echo "Usage: $0 <backup-file.rdb.gz>"
    echo ""
    echo "Examples:"
    echo "  $0 ./backups/redis/dump_20260219_120000.rdb.gz"
    echo "  $0 ./backups/redis/dump_20260219_120000.rdb"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/redis/*.rdb* 2>/dev/null || echo "  (no backups found)"
    exit 0
fi

BACKUP_FILE="$1"

echo "🔄 Redis Restore"
echo "================"
echo ""

# Check if file exists
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Check if Redis is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    print_warning "Redis container is not running"
    read -p "Start Redis first? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        docker-compose up -d redis
        echo "Waiting for Redis to start..."
        sleep 5
    else
        exit 1
    fi
fi

# Confirm restore
print_warning "This will REPLACE all current Redis data!"
read -p "Are you sure you want to continue? (yes/no): " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Restore cancelled"
    exit 0
fi

echo ""
echo "Restoring from: $BACKUP_FILE"
echo ""

# Handle compressed files
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "📦 Decompressing backup..."
    TEMP_FILE="/tmp/restore_$(date +%s).rdb"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Stop Redis
echo "🛑 Stopping Redis..."
docker-compose stop redis
print_status "Redis stopped"

# Backup current data first (safety)
echo ""
echo "💾 Creating safety backup of current data..."
SAFETY_BACKUP="./backups/redis/safety_$(date +%Y%m%d_%H%M%S).rdb"
mkdir -p "./backups/redis"
docker cp "$CONTAINER_NAME:/data/dump.rdb" "$SAFETY_BACKUP" 2>/dev/null || true
print_status "Safety backup created"

# Restore data file
echo ""
echo "📂 Copying backup to container..."
docker cp "$RESTORE_FILE" "$CONTAINER_NAME:/data/dump.rdb"
print_status "Backup file copied"

# Fix permissions
echo ""
echo "🔧 Fixing permissions..."
docker exec "$CONTAINER_NAME" chown redis:redis /data/dump.rdb

# Start Redis
echo ""
echo "🚀 Starting Redis..."
docker-compose start redis

# Wait for Redis to be ready
echo ""
echo "⏳ Waiting for Redis to be ready..."
for i in {1..30}; do
    if docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" ping 2>/dev/null | grep -q "PONG"; then
        break
    fi
    echo "   Waiting... ($i/30)"
    sleep 1
done

# Verify restore
echo ""
echo "🔍 Verifying restore..."
if docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" ping | grep -q "PONG"; then
    print_status "Redis is responding!"
    
    # Show key count
    KEY_COUNT=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" DBSIZE 2>/dev/null || echo "0")
    print_info "Total keys in database: $KEY_COUNT"
    
    # Show project-specific keys
    PROJECT_KEYS=$(docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" EVAL "local keys = redis.call('keys', 'project:*'); return #keys" 0 2>/dev/null || echo "0")
    print_info "Project-prefixed keys: $PROJECT_KEYS"
else
    print_error "Redis is not responding after restore"
    exit 1
fi

# Cleanup temp file
if [ -n "$TEMP_FILE" ] && [ -f "$TEMP_FILE" ]; then
    rm -f "$TEMP_FILE"
fi

echo ""
echo "================"
print_status "Restore complete!"
echo ""
echo "💡 Safety backup: $SAFETY_BACKUP"
echo "🧹 To clean up safety backup: rm $SAFETY_BACKUP"
echo ""
