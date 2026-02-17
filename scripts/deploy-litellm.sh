#!/bin/bash
# LiteLLM Deployment Script for server62
# Usage: GROQ_API_KEY=xxx LITELLM_MASTER_KEY=yyy ./scripts/deploy-litellm.sh

set -e

SERVER="100.91.164.109"
PORT=20
USER="admin"
LITELLM_DIR="/opt/litellm"

echo "=== LiteLLM Deployment to server62 ==="

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "Error: GROQ_API_KEY not set"
    echo "Set it with: export GROQ_API_KEY=gsk_xxx"
    exit 1
fi

if [ -z "$LITELLM_MASTER_KEY" ]; then
    LITELLM_MASTER_KEY="litellm_change_me"
fi

# Create remote directory
echo "[1/5] Creating remote directory..."
ssh -o StrictHostKeyChecking=no -p $PORT $USER@$SERVER "mkdir -p $LITELLM_DIR"

# Copy config files
echo "[2/5] Copying configuration files..."
scp -o StrictHostKeyChecking=no -P $PORT litellm/proxy_config.yaml $USER@$SERVER:$LITELLM_DIR/

# Create .env on remote
echo "[3/5] Setting up environment..."
ssh -o StrictHostKeyChecking=no -p $PORT $USER@$SERVER "cd $LITELLM_DIR && echo 'GROQ_API_KEY=$GROQ_API_KEY' > .env && echo 'LITELLM_MASTER_KEY=$LITELLM_MASTER_KEY' >> .env"

# Install and configure LiteLLM
echo "[4/5] Installing and configuring LiteLLM..."
ssh -o StrictHostKeyChecking=no -p $PORT $USER@$SERVER << 'ENDSSH'
set -e
cd /opt/litellm

# Install LiteLLM if needed
if ! command -v litellm &> /dev/null; then
    pip install litellm[proxy] --break-system-packages
fi

# Create PM2 config
cat > ecosystem.config.js << 'PMEOF'
module.exports = {
  apps: [{
    name: 'litellm',
    script: 'litellm',
    args: '--config proxy_config.yaml --port 4000 --host 0.0.0.0',
    cwd: '/opt/litellm',
    interpreter: 'none',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: { NODE_ENV: 'production' }
  }]
};
PMEOF

# Restart PM2
pm2 restart litellm 2>/dev/null || pm2 start ecosystem.config.js
pm2 save
pm2 list

echo "LiteLLM installed and started!"
ENDSSH

# Wait for startup
sleep 5

# Verify
echo "[5/5] Verifying deployment..."
ssh -o StrictHostKeyChecking=no -p $PORT $USER@$SERVER "curl -s http://localhost:4000/health" || echo "Warning: Health check may have failed"

echo ""
echo "=== Deployment Complete ==="
echo "LiteLLM should be running at: http://$SERVER:4000"
echo ""
echo "To test manually:"
echo "  curl -X POST http://$SERVER:4000/v1/chat/completions \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"model\":\"groq/llama-3.3-70b-versatile\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}],\"max_tokens\":20}'"
