# Performance Audit Report

**Date**: 2026-02-17  
**URL**: https://marketing.tvoje.info  
**Lighthouse Version**: 13.0.3

---

## Summary

| Metric      | Score | Target | Status  |
| ----------- | ----- | ------ | ------- |
| Performance | 100   | ≥95    | ✅ PASS |
| LCP         | 1.9s  | <2.5s  | ✅ PASS |
| CLS         | 0.001 | <0.1   | ✅ PASS |
| TBT         | 60ms  | <200ms | ✅ PASS |
| Speed Index | 1.3s  | -      | ✅      |
| TTI         | 1.9s  | -      | ✅      |

---

## Key Metrics

| Metric                   | Value | Rating |
| ------------------------ | ----- | ------ |
| First Contentful Paint   | 1.0s  | Good   |
| Largest Contentful Paint | 1.9s  | Good   |
| Speed Index              | 1.3s  | Good   |
| Time to Interactive      | 1.9s  | Good   |
| Total Blocking Time      | 60ms  | Good   |
| Cumulative Layout Shift  | 0.001 | Good   |

---

## Issues Found

### Critical Issues

| Issue                       | Details                               | Impact                  |
| --------------------------- | ------------------------------------- | ----------------------- |
| 404: `/scripts/interactive` | Missing script resource               | Medium                  |
| 404: `/favicon.ico`         | Missing favicon                       | Low                     |
| Mixed Content               | HTTP prefetch to `/projects/` blocked | Medium                  |
| SyntaxError                 | `import.meta` outside module          | High - JavaScript error |

### Warnings

- None significant

---

## Network Requests

- **Total Requests**: 12
- **Total Transfer Size**: 402 KB
- **Main Document**: 15 KB

### Resources

| Type      | Count | Size   |
| --------- | ----- | ------ |
| Images    | 2     | 177 KB |
| Fonts     | 2     | 134 KB |
| CSS       | 2     | 64 KB  |
| Scripts   | 1     | 2 KB   |
| Documents | 2     | 30 KB  |

---

## Recommendations

1. **Fix 404 errors**: Add favicon.ico and remove reference to `/scripts/interactive`
2. **Fix JavaScript error**: Review inline scripts for `import.meta` usage
3. **Mixed content**: Update any HTTP links to HTTPS

---

## Conclusion

**Status**: ✅ PASS (with minor issues)

All core web vitals pass targets. The main concerns are 404 errors and a JavaScript error that should be investigated.
