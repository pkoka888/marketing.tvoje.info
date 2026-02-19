#!/bin/bash

echo "=== Marketing Website Setup ==="
echo "[1/4] Checking Node.js..."
node --version && npm --version

if [ ! -d node_modules ]; then
    echo "[2/4] Installing dependencies..."
    npm install
else
    echo "[2/4] Dependencies already installed"
fi

echo "[3/4] Starting Astro dev server on http://localhost:4321..."
npm run dev
