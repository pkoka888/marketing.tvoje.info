#Requires -Version 5.1
<#
.SYNOPSIS
    Cache Cleanup Script for Windows (PowerShell)
.DESCRIPTION
    Cleans various caches to free space and fix issues
.NOTES
    Run as Administrator for best results
#>

Write-Host "🧹 Cache Cleanup Script (PowerShell)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Clean npm cache
Write-Host "📦 Cleaning npm cache..." -ForegroundColor Yellow
try {
    npm cache clean --force 2>$null
    Write-Host "  ✅ npm cache cleaned" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  npm cache clean failed or not needed" -ForegroundColor Yellow
}

# 2. Clean node_modules/.cache
Write-Host ""
Write-Host "🗑️  Cleaning node_modules/.cache..." -ForegroundColor Yellow
if (Test-Path "node_modules/.cache") {
    Remove-Item -Path "node_modules/.cache" -Recurse -Force
    Write-Host "  ✅ node_modules/.cache removed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  node_modules/.cache not found" -ForegroundColor Yellow
}

# 3. Clean Astro cache
Write-Host ""
Write-Host "🚀 Cleaning Astro cache..." -ForegroundColor Yellow
if (Test-Path ".astro") {
    Remove-Item -Path ".astro" -Recurse -Force
    Write-Host "  ✅ .astro cache removed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  .astro cache not found" -ForegroundColor Yellow
}

# 4. Clean dist/build directories
Write-Host ""
Write-Host "🏗️  Cleaning build directories..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
    Write-Host "  ✅ dist/ removed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  dist/ not found" -ForegroundColor Yellow
}

# 5. Clean temporary files
Write-Host ""
Write-Host "🧹 Cleaning temporary files..." -ForegroundColor Yellow
$tempFiles = Get-ChildItem -Path "." -Filter "*.tmp" -Recurse -ErrorAction SilentlyContinue
$tempFiles | Remove-Item -Force -ErrorAction SilentlyContinue
$logFiles = Get-ChildItem -Path "." -Filter "*.log" -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) }
$logFiles | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "  ✅ Temporary files cleaned" -ForegroundColor Green

# 6. Clean VSCode cache
Write-Host ""
Write-Host "💻 Cleaning VSCode caches..." -ForegroundColor Yellow
$vscodeCache = "$env:APPDATA\Code\Cache"
if (Test-Path $vscodeCache) {
    Write-Host "  ℹ️  VSCode cache found at: $vscodeCache" -ForegroundColor Cyan
    Write-Host "     Clear manually if needed" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ Cache cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Run 'npm ci' to reinstall dependencies if needed"
Write-Host "   - Run 'npm run build' to rebuild the project"
Write-Host ""
