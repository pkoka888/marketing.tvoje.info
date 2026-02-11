#!/bin/bash
# Project Validator Script
# Runs Cline CLI in headless mode for background validation
# Usage: ./scripts/validate.sh [full|quick|audit|errors]
#
# Modes:
#   quick  - Build + test + lint (default)
#   full   - All validation checks per .clinerules/validator.md
#   audit  - Agent self-audit per .clinerules/agent-audit.md
#   errors - Error scan per .clinerules/error-watcher.md

set -euo pipefail

MODE=${1:-quick}
TIMESTAMP=$(date +%Y-%m-%d)
REPORT_DIR="plans/agent-shared"

case "$MODE" in
  quick)
    echo "🔍 Running quick validation..."
    npm run build 2>&1 | tee "${REPORT_DIR}/validation-reports/${TIMESTAMP}-build.log"
    npm run test 2>&1 | tee "${REPORT_DIR}/validation-reports/${TIMESTAMP}-test.log"
    npm run format:check 2>&1 | tee "${REPORT_DIR}/validation-reports/${TIMESTAMP}-format.log"
    echo "✅ Quick validation complete. Reports in ${REPORT_DIR}/validation-reports/"
    ;;
  full)
    echo "🔍 Running full validation via Cline CLI..."
    if command -v cline &> /dev/null; then
      cline -y --task "Run full project validation per .clinerules/validator.md. Save report to ${REPORT_DIR}/validation-reports/${TIMESTAMP}-validation-full.md"
    else
      echo "⚠️ Cline CLI not found. Running manual validation..."
      npm run build 2>&1
      npm run test 2>&1
      npm run format:check 2>&1
      npx eslint src/ --config eslint.config.mjs 2>&1
      echo "Manual validation complete."
    fi
    ;;
  audit)
    echo "🔍 Running agent audit via Cline CLI..."
    if command -v cline &> /dev/null; then
      cline -y --task "Run agent self-audit per .clinerules/agent-audit.md. Save report to ${REPORT_DIR}/audit-reports/${TIMESTAMP}-agent-audit.md"
    else
      echo "⚠️ Cline CLI not found. Manual audit not available."
      exit 1
    fi
    ;;
  errors)
    echo "🔍 Running error scan via Cline CLI..."
    if command -v cline &> /dev/null; then
      cline -y --task "Run error scan per .clinerules/error-watcher.md. Save report to ${REPORT_DIR}/error-logs/${TIMESTAMP}-error-scan.md"
    else
      echo "⚠️ Cline CLI not found. Running basic error check..."
      npm run build 2>&1 | grep -i "error\|warn" || echo "No build errors."
      npm run test 2>&1 | grep -i "fail\|error" || echo "No test errors."
      echo "Basic error check complete."
    fi
    ;;
  *)
    echo "Usage: ./scripts/validate.sh [quick|full|audit|errors]"
    exit 1
    ;;
esac
