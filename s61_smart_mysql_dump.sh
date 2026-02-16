#!/bin/bash
# Smart MySQL Dump with PrestaShop Optimizations
# Ansible managed

set -euo pipefail

# Configuration
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER="${DB_USER:-backup_user}"
DB_PASS="${DB_PASS:-backup_pass}"
DB_NAME="${DB_NAME:-prestashop}"
BACKUP_DIR="/var/backups/server-infra-gem/okamih/databases"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql.gz"
STRUCTURE_FILE="${BACKUP_DIR}/${DB_NAME}_structure_${TIMESTAMP}.sql.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Build exclusion arguments for mysqldump
EXCLUDE_ARGS=""
for table in ps_connections ps_connections_source ps_guest ps_statssearch ps_layered_filter ps_layered_cache; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --ignore-table=${DB_NAME}.${table}"
done

# Build pattern exclusions (for dynamic tables)
PATTERN_EXCLUDES=""
for pattern in ps_smarty_cache_* ps_connections_*; do
    # Get matching table names from database
    TABLE_LIST=$(mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "SHOW TABLES LIKE '${pattern}';" "$DB_NAME" 2>/dev/null | tail -n +2)
    for table in $TABLE_LIST; do
        PATTERN_EXCLUDES="$PATTERN_EXCLUDES --ignore-table=${DB_NAME}.${table}"
    done
done

echo "Starting smart MySQL backup for $DB_NAME..."
echo "Excluding tables: ps_connections, ps_connections_source, ps_guest, ps_statssearch, ps_layered_filter, ps_layered_cache"
echo "Pattern exclusions: ps_smarty_cache_*, ps_connections_*"

# Enterprise mysqldump with best practices
mysqldump --host="$DB_HOST" \
          --port="$DB_PORT" \
          --user="$DB_USER" \
          --password="$DB_PASS" \
          --single-transaction \
          --routines \
          --triggers \
          --quick \
          --skip-lock-tables \
          --max-allowed-packet=1G \
          --net-buffer-length=32768 \
          $EXCLUDE_ARGS \
          $PATTERN_EXCLUDES \
          "$DB_NAME" | gzip -9 > "$BACKUP_FILE"

echo "Database backup completed: $BACKUP_FILE"

# Create structure-only backup for excluded tables
echo "Creating structure backup for excluded tables..."
mysqldump --host="$DB_HOST" \
          --port="$DB_PORT" \
          --user="$DB_USER" \
          --password="$DB_PASS" \
          --no-data \
          $EXCLUDE_ARGS \
          $PATTERN_EXCLUDES \
          "$DB_NAME" | gzip -9 > "$STRUCTURE_FILE"

echo "Structure backup completed: $STRUCTURE_FILE"

# Validate backup integrity
echo "Validating backup integrity..."
if ! gzip -t "$BACKUP_FILE"; then
    echo "ERROR: Backup file corruption detected!"
    rm -f "$BACKUP_FILE" "$STRUCTURE_FILE"
    exit 1
fi

# Test database connectivity
if ! mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "SELECT 1;" "$DB_NAME" >/dev/null; then
    echo "ERROR: Database connectivity test failed!"
    exit 1
fi

echo "Backup validation successful!"
echo "Files created:"
echo "  Data: $BACKUP_FILE"
echo "  Structure: $STRUCTURE_FILE"
