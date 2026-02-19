#!/bin/bash
#
# Redis Backup Script
# Backs up Redis data to local backups directory
#

set -e

# Configuration
BACKUP_DIR="./backups/redis"
CONTAINER_NAME="marketing-redis"
REDIS_PASSWORD="marketing"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

echo "💾 Redis Backup Script"
echo "======================"
echo ""

# Check if Redis is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    print_error "Redis container ($CONTAINER_NAME) is not running"
    echo "Start it first: docker-compose up -d redis"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "Creating backup: $DATE"
echo ""

# Method 1: Trigger BGSAVE and copy RDB
echo "📦 Creating RDB snapshot..."
docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" BGSAVE

# Wait for save to complete
echo "   Waiting for background save..."
sleep 2

while docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" INFO persistence | grep -q "rdb_bgsave_in_progress:1"; do
    echo "   Still saving..."
    sleep 1
done

# Copy RDB file
docker cp "$CONTAINER_NAME:/data/dump.rdb" "$BACKUP_DIR/dump_$DATE.rdb"
print_status "RDB backup created: dump_$DATE.rdb"

# Method 2: Backup AOF if it exists
if docker exec "$CONTAINER_NAME" test -f /data/appendonly.aof 2>/dev/null; then
    echo ""
    echo "📄 Backing up AOF file..."
    docker cp "$CONTAINER_NAME:/data/appendonly.aof" "$BACKUP_DIR/appendonly_$DATE.aof"
    print_status "AOF backup created: appendonly_$DATE.aof"
fi

# Method 3: Export key list
echo ""
echo "📝 Exporting key list..."
docker exec "$CONTAINER_NAME" redis-cli -a "$REDIS_PASSWORD" --scan --pattern "*" > "$BACKUP_DIR/keys_$DATE.txt"
print_status "Key list exported: keys_$DATE.txt"

# Compress backups
echo ""
echo "🗜️  Compressing backups..."
gzip -f "$BACKUP_DIR/dump_$DATE.rdb" 2>/dev/null || true
gzip -f "$BACKUP_DIR/appendonly_$DATE.aof" 2>/dev/null || true
print_status "Backups compressed"

# Cleanup old backups
echo ""
echo "🧹 Cleaning up old backups (retention: $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "*.gz" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "keys_*.txt" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
print_status "Old backups cleaned"

# Show backup summary
echo ""
echo "======================"
print_status "Backup complete!"
echo ""
echo "📁 Backup location: $BACKUP_DIR"
echo "📊 Backup size:"
du -h "$BACKUP_DIR"/*$DATE* 2>/dev/null || echo "   (files compressed)"
echo ""
echo "💡 To restore, use: scripts/restore-redis.sh"
echo ""
