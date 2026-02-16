#!/bin/bash
#===============================================================================
# Smart Backup Script for Server61 -> Server60
# Excludes: img/, cache/, logs/, vendor/
# Sequential backup: okamih.cz first, then okamih.sk
# Direct transfer to server60 backup hub
#===============================================================================

set -e

# Configuration
BACKUP_USER="agent"
BACKUP_DEST_SERVER="192.168.1.60"
BACKUP_DEST_PATH="/var/backups/server61"
BACKUP_DATE=$(date +%Y-%m-%d)
TEMP_BACKUP_DIR="/tmp/backup-${BACKUP_DATE}"
LOG_FILE="/var/log/smart-backup-server60.log"

# MySQL credentials (moved to /root/.my.cnf)
MY_CNF="/root/.my.cnf"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

log "=========================================="
log "Smart Backup Started"
log "=========================================="

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
log "Current disk usage: ${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 90 ]; then
    error_exit "Disk usage is ${DISK_USAGE}% - too high to create backups safely"
fi

# Create temporary backup directory
mkdir -p "$TEMP_BACKUP_DIR"
log "Created temporary backup directory: $TEMP_BACKUP_DIR"

# ==========================================
# BACKUP OKAMIH.CZ
# ==========================================
log "Starting okamih.cz backup..."

# Database backup
log "  Backing up okamih_shop database..."
mysqldump --defaults-extra-file="$MY_CNF" okamih_shop 2>/dev/null | \
    gzip > "$TEMP_BACKUP_DIR/okamih_cz_db.sql.gz" || error_exit "Failed to backup okamih.cz database"
DB_SIZE=$(du -sh "$TEMP_BACKUP_DIR/okamih_cz_db.sql.gz" | cut -f1)
log "  Database backup complete: $DB_SIZE"

# WWW backup (excluding img/cache)
log "  Backing up okamih.cz www (excluding img/cache)..."
tar --exclude='*/img/*' \
    --exclude='*/images/*' \
    --exclude='*/cache/*' \
    --exclude='*/var/cache/*' \
    --exclude='*/var/logs/*' \
    --exclude='*/vendor/*' \
    --exclude='*.log' \
    -czf "$TEMP_BACKUP_DIR/okamih_cz_www.tar.gz" \
    -C /var/www/okamih.cz www || error_exit "Failed to backup okamih.cz www"
WWW_SIZE=$(du -sh "$TEMP_BACKUP_DIR/okamih_cz_www.tar.gz" | cut -f1)
log "  WWW backup complete: $WWW_SIZE"

# Transfer to server60
log "  Transferring okamih.cz backups to server60..."
ssh -i /root/.ssh/id_ed25519 -p 20 "$BACKUP_USER@$BACKUP_DEST_SERVER" \
    "mkdir -p $BACKUP_DEST_PATH/$BACKUP_DATE" || error_exit "Failed to create remote directory"

rsync -avz -e "ssh -i /root/.ssh/id_ed25519 -p 20" \
    "$TEMP_BACKUP_DIR/okamih_cz_"* \
    "$BACKUP_USER@$BACKUP_DEST_SERVER:$BACKUP_DEST_PATH/$BACKUP_DATE/" || error_exit "Failed to transfer okamih.cz backups"
log "  Transfer complete"

# Remove local copies
rm -f "$TEMP_BACKUP_DIR/okamih_cz_"*
log "  Removed local okamih.cz backups"

# ==========================================
# BACKUP OKAMIH.SK
# ==========================================
log "Starting okamih.sk backup..."

# Database backup
log "  Backing up okamih_shop_sk database..."
mysqldump --defaults-extra-file="$MY_CNF" okamih_shop_sk 2>/dev/null | \
    gzip > "$TEMP_BACKUP_DIR/okamih_sk_db.sql.gz" || error_exit "Failed to backup okamih.sk database"
DB_SIZE=$(du -sh "$TEMP_BACKUP_DIR/okamih_sk_db.sql.gz" | cut -f1)
log "  Database backup complete: $DB_SIZE"

# WWW backup (excluding img/cache)
log "  Backing up okamih.sk www (excluding img/cache)..."
tar --exclude='*/img/*' \
    --exclude='*/images/*' \
    --exclude='*/cache/*' \
    --exclude='*/var/cache/*' \
    --exclude='*/var/logs/*' \
    --exclude='*/vendor/*' \
    --exclude='*.log' \
    -czf "$TEMP_BACKUP_DIR/okamih_sk_www.tar.gz" \
    -C /var/www/okamih.sk www || error_exit "Failed to backup okamih.sk www"
WWW_SIZE=$(du -sh "$TEMP_BACKUP_DIR/okamih_sk_www.tar.gz" | cut -f1)
log "  WWW backup complete: $WWW_SIZE"

# Transfer to server60
log "  Transferring okamih.sk backups to server60..."
rsync -avz -e "ssh -i /root/.ssh/id_ed25519 -p 20" \
    "$TEMP_BACKUP_DIR/okamih_sk_"* \
    "$BACKUP_USER@$BACKUP_DEST_SERVER:$BACKUP_DEST_PATH/$BACKUP_DATE/" || error_exit "Failed to transfer okamih.sk backups"
log "  Transfer complete"

# Remove local copies
rm -f "$TEMP_BACKUP_DIR/okamih_sk_"*
log "  Removed local okamih.sk backups"

# ==========================================
# BACKUP NGINX CONFIGS
# ==========================================
log "Backing up nginx configurations..."
tar -czf "$TEMP_BACKUP_DIR/nginx_configs.tar.gz" \
    -C /etc nginx/sites-available nginx/sites-enabled nginx/nginx.conf || error_exit "Failed to backup nginx configs"
NGINX_SIZE=$(du -sh "$TEMP_BACKUP_DIR/nginx_configs.tar.gz" | cut -f1)
log "  Nginx backup complete: $NGINX_SIZE"

# Transfer to server60
rsync -avz -e "ssh -i /root/.ssh/id_ed25519 -p 20" \
    "$TEMP_BACKUP_DIR/nginx_configs.tar.gz" \
    "$BACKUP_USER@$BACKUP_DEST_SERVER:$BACKUP_DEST_PATH/$BACKUP_DATE/" || error_exit "Failed transfer nginx configs"
log "  Transfer complete"

# Remove local copy
rm -f "$TEMP_BACKUP_DIR/nginx_configs.tar.gz"

# ==========================================
# CLEANUP
# ==========================================
log "Cleaning up..."
rmdir "$TEMP_BACKUP_DIR" 2>/dev/null || true

# Create completion marker on server60
ssh -i /root/.ssh/id_ed25519 -¤ 20 "$BACKUP_USER@$BACKUP_DEST_SERVER" \
    "echo 'Backup completed: $(date --iso-8601=seconds)' > $BACKUP_DEST_PATH/$BACKUP_DATE/BACKUP_COMPLETE"

# Final disk usage
FINAL_DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
log "Final disk usage: ${FINAL_DISK_USAGE}%"

log "=========================================="
log "âœ… Backup Completed Successfully"
log "Destination: $BACKUP_USER@$BACKUP_DEST_SERVER:$BACKUP_DEST_PATH/$BACKUP_DATE/"
log "=========================================="
