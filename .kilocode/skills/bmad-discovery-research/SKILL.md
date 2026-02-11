---
name: bmad-discovery-research
description: Conducts comprehensive market and technical research for new initiatives.
allowed-tools: ["Read", "Write", "Grep", "Bash", "Fetch"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "research competitors"
      - "market analysis"
      - "technical feasibility"
      - "explore options"
      - "best practices"
      - "compare solutions"
      - "industry standards"
      - "competitor analysis"
      - "user research"
    keywords:
      - research
      - analysis
      - market
      - competitor
      - benchmark
      - feasibility
      - explore
  capabilities:
    - market-research
    - competitor-analysis
    - technical-feasibility
    - user-research
    - best-practices
    - technology-evaluation
  prerequisites: []
  outputs:
    - research-report
    - findings-summary
    - recommendations
---

# BMAD Discovery Research Skill

## When to Invoke

Use this skill when the user:
- Needs to research competitors, markets, or technology options.
- Wants to evaluate technical feasibility or new tools.
- Is exploring best practices or industry standards.
- Requires data-driven recommendations for decision-making.
- Needs user research or persona development.

Do not invoke for implementation planning (use `bmad-product-planning`) or architectural decisions (use `bmad-architecture-design`).

## Mission

Deliver actionable research insights that inform product, technical, and strategic decisions. Provide evidence-based recommendations with clear trade-offs.

## Inputs Required

- Research objective or question to answer.
- Scope (market segment, technologies, competitors to evaluate).
- Success criteria for the research.
- Any existing data or constraints to consider.

## Outputs

- **Research report** with findings, evidence, and sources.
- **Findings summary** with key insights and implications.
- **Recommendations** with trade-offs and next steps.

## Process

1. Define research scope, questions, and success criteria.
2. Conduct primary and secondary research.
3. Analyze findings and identify patterns.
4. Synthesize recommendations with evidence.
5. Document limitations and areas for further research.

## Quality Gates

- Research has clear, answerable questions.
- Multiple sources are consulted with conflicting views represented.
- Recommendations are evidence-based with explicit trade-offs.
- Limitations and uncertainties are documented.

## Error Handling

- If insufficient data is available, document gaps and suggest research methods.
- If scope is too broad, prioritize and propose focused approach.
- If findings conflict, present multiple perspectives with confidence levels.

## Deliverable Structure

```
research-report/
├── executive-summary.md
├── methodology.md
├── findings.md
├── analysis.md
├── recommendations.md
├── appendices/
│   ├── sources.md
│   └── data-tables.md
```
