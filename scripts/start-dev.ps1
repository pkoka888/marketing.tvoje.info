# Marketing Website - VS Code Startup Script
# Run this to set up the development environment

Write-Host "=== Marketing Website Setup ===" -ForegroundColor Cyan

# Check Node.js
Write-Host "`n[1/4] Checking Node.js..." -ForegroundColor Yellow
node --version
npm --version

# Install dependencies if needed
if (-not (Test-Path node_modules)) {
    Write-Host "`n[2/4] Installing dependencies..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "`n[2/4] Dependencies already installed" -ForegroundColor Green
}

# Start dev server
Write-Host "`n[3/4] Starting Astro dev server..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:4321" -ForegroundColor Cyan

# Run in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\pavel\projects\marketing.tvoje.info'; npm run dev"

Write-Host "`n[4/4] Dev server starting..." -ForegroundColor Green
Write-Host "`n=== Ready ===" -ForegroundColor Cyan
Write-Host "Open: http://localhost:4321" -ForegroundColor White
