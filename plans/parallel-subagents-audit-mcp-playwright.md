# Parallel Subagents Plan: Audit, MCP Alignment, Playwright & Visual Verification

**Created:** 2026-02-13
**Version:** 1.0
**Status:** Plan (Ready for Implementation)
**Format:** Hybrid BMAD Orchestration

---

## Executive Summary

This plan defines a parallel subagent execution framework for comprehensive app auditing, MCP server alignment, Playwright test enhancement with Chromium debugging, and visual verification workflows. The plan uses BMAD methodology to structure 4 specialized agents working in parallel.

| Component                       | Status  | Priority |
| ------------------------------- | ------- | -------- |
| App Audit                       | Planned | P1       |
| MCP Alignment for OpenCode      | Planned | P1       |
| Playwright + Chromium Debugging | Planned | P2       |
| Visual Verification Workflow    | Planned | P2       |

---

## BMAD Framework Application

### Project Level: **2** (Medium feature set - multiple agents + integration)

### Phase Structure

| Phase             | Agent              | Task                           |
| ----------------- | ------------------ | ------------------------------ |
| 1. Analysis       | Auditor Agent      | Audit app, gather requirements |
| 2. Planning       | Configurator Agent | MCP alignment, OpenCode config |
| 3. Solutioning    | Integrator Agent   | Playwright debugging setup     |
| 4. Implementation | Tester Agent       | Visual verification execution  |

---

## Agent Definitions

### Agent 1: Auditor Agent

**Role:** Comprehensive application audit

**Skills Required:**

- Security audit (`.kilocode/skills/bmad-security-review/`)
- Performance optimization (`.kilocode/skills/bmad-performance-optimization/`)
- Accessibility WCAG (`.kilocode/skills/accessibility-wcag/`)

**Rules:**

- `.clinerules/validator.md` - Validation checks
- `.clinerules/accessibility-rules.md` - A11y compliance
- `.agents/rules/rule-duplication.md` - Cross-agent consistency

**Workflow:**

1. Run security audit (npm audit, dependency check)
2. Execute accessibility audit (Lighthouse, WCAG)
3. Check performance metrics
4. Validate build process
5. Document findings

**Deliverables:**

- `plans/audit-findings-[date].md`
- `evidence/security-report.md`
- `evidence/a11y-report.md`

---

### Agent 2: Configurator Agent

**Role:** MCP server alignment for OpenCode

**Skills Required:**

- Provider fallback (`.kilocode/skills/provider-fallback/`)
- LiteLLM debugging (`.kilocode/skills/litellm-debug/`)

**Rules:**

- `.clinerules/error-watcher.md` - Error detection
- `.agents/rules/server-preservation.md` - Server preservation

**Workflow:**

1. Review current MCP configuration (`.kilocode/mcp.json`)
2. Align OpenCode instructions (opencode.json)
3. Add Playwright MCP server configuration
4. Configure Chromium debugging settings
5. Test MCP server connectivity

**Deliverables:**

- Updated `opencode.json` with MCP rules
- New MCP server configs in `.kilocode/mcp.json`
- `plans/mcp-playwright-alignment.md`

---

### Agent 3: Integrator Agent

**Role:** Playwright enhancement with Chromium debugging

**Skills Required:**

- Test strategy (`.kilocode/skills/bmad-test-strategy/`)
- Astro portfolio (`.kilocode/skills/astro-portfolio/`)

**Rules:**

- `.clinerules/98-visual-verification.md` - Visual verification mandate

**Workflow:**

1. Enhance `playwright.config.ts` for debugging
2. Configure Chromium CDP (Chrome DevTools Protocol) access
3. Add debugging utilities to test suite
4. Create debug helper scripts
5. Configure screenshot capture for visual tests

**Playwright Debugging Configuration:**

```typescript
// playwright.config.ts enhancements
use: {
  launchOptions: {
    devtools: true, // Open Chromium DevTools
    args: [
      '--auto-open-devtools-for-tabs',
      '--enable-precise-memory-info'
    ]
  },
  contextOptions: {
    viewport: { width: 1280, height: 720 }
  }
}
```

**Deliverables:**

- Enhanced `playwright.config.ts`
- Debug utilities in `tests/debug/`
- `tests/e2e/debug.spec.ts`

---

### Agent 4: Tester Agent

**Role:** Visual verification and functional confirmation

**Skills Required:**

- Visual verification (`.clinerules/98-visual-verification.md`)
- i18n content (`.kilocode/skills/i18n-content/`)

**Rules:**

- `.clinerules/98-visual-verification.md` - Mandatory visual checks

**Workflow:**

1. Run Playwright tests with screenshots
2. Capture evidence in `evidence/` directory
3. Verify EN and CS language variants
4. Compare visual outputs against baselines
5. Document test results

**Evidence Structure:**

```
evidence/
├── audit-[date]/
│   ├── homepage-en.png
│   ├── homepage-cs.png
│   └── mobile-view.png
├── visual-[feature]/
│   ├── light-mode.png
│   └── dark-mode.png
└── debug-screenshots/
    ├── console-output.png
    └── network-log.png
```

**Deliverables:**

- Visual evidence in `evidence/`
- Test report `plans/visual-verification-report.md`

---

## Parallel Execution Matrix

| Agent        | Dependencies              | Can Run In Parallel With         |
| ------------ | ------------------------- | -------------------------------- |
| Auditor      | None                      | Configurator, Integrator, Tester |
| Configurator | Auditor (findings)        | Auditor, Integrator, Tester      |
| Integrator   | Configurator (MCP config) | Auditor                          |
| Tester       | Auditor, Integrator       | Auditor, Configurator            |

**Recommended Parallel Groups:**

- **Group A:** Auditor + Configurator (independent start)
- **Group B:** Integrator (waits for Configurator)
- **Group C:** Tester (waits for Auditor + Integrator)

---

## BMAD Decision Points

### Decision 1: MCP Server Selection

| Option                | Pros              | Cons             | Recommendation  |
| --------------------- | ----------------- | ---------------- | --------------- |
| Use existing bmad-mcp | Already installed | Limited coverage | Start with this |
| Add Playwright MCP    | Native testing    | New integration  | Recommended     |
| Use npx playwright    | No config needed  | Less control     | Fallback        |

**Decision:** Use bmad-mcp + new Playwright configuration

### Decision 2: Chromium Debugging Approach

| Option             | Pros                 | Cons                |
| ------------------ | -------------------- | ------------------- |
| CDP via Playwright | Native support       | Requires setup      |
| External DevTools  | Full Chrome features | Manual intervention |
| Screenshot capture | Visual verification  | No live debugging   |

**Decision:** CDP + screenshot capture hybrid

---

## Risk Assessment

| Risk                         | Likelihood | Impact | Mitigation             |
| ---------------------------- | ---------- | ------ | ---------------------- |
| MCP server conflict          | Medium     | High   | Use project isolation  |
| Playwright timeout           | Low        | Medium | Increase test timeouts |
| Visual diff false positives  | High       | Low    | Use human verification |
| Cross-language inconsistency | Medium     | Medium | Run both EN/CS tests   |

---

## Implementation Checklist

### Auditor Agent

- [ ] Run `npm audit` and document vulnerabilities
- [ ] Execute accessibility audit with Lighthouse
- [ ] Check i18n content completeness
- [ ] Validate build with `npm run build`
- [ ] Document all findings

### Configurator Agent

- [ ] Review current MCP configuration
- [ ] Add Playwright MCP server
- [ ] Update opencode.json instructions
- [ ] Test MCP connectivity
- [ ] Document configuration

### Integrator Agent

- [ ] Configure Chromium devtools in playwright.config.ts
- [ ] Create debug test utilities
- [ ] Add screenshot helpers
- [ ] Test debug functionality
- [ ] Document debugging guide

### Tester Agent

- [ ] Run full test suite with screenshots
- [ ] Capture EN and CS versions
- [ ] Verify visual components
- [ ] Create verification report
- [ ] Archive evidence

---

## Success Metrics

| Metric              | Target        | Measurement         |
| ------------------- | ------------- | ------------------- |
| Audit coverage      | 100%          | All checks executed |
| MCP alignment       | 10/10 servers | Connectivity test   |
| Visual verification | All pages     | Screenshot capture  |
| Build passing       | 0 errors      | npm run build       |

---

## Related Documentation

| Document                                 | Purpose                   |
| ---------------------------------------- | ------------------------- |
| `plans/mcp-server-consolidation-plan.md` | Existing MCP config       |
| `plans/enhanced-audit-plan-v2.md`        | Previous audit work       |
| `.clinerules/98-visual-verification.md`  | Visual verification rules |
| `playwright.config.ts`                   | Current Playwright config |

---

## Next Steps

1. **Initialize parallel execution** - Launch Auditor + Configurator simultaneously
2. **Monitor progress** - Check agent status every 15 minutes
3. **Handle blockers** - Address MCP conflicts immediately
4. **Complete integration** - Run Integrator after Configurator
5. **Final verification** - Execute Tester after others complete
6. **Document results** - Create consolidated report

---

_Plan created using BMAD methodology with parallel subagent orchestration._
