# BMAD Orchestrator - Enhanced Multi-Agent System

## Workspace: bmad-orchestration

**Mode**: Parallel Agents + Phased Files + Approval Gates
**LiteLLM Routing**: groq/\* default (speed/cheap); anthropic/claude-opus-4-2025-06-20 for PRD/strategy; gemini/gemini-2-5-pro-exp-06-05 for SERP research

---

## Agent Team Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEAD ORCHESTRATOR                             │
│              (Gemini 3 Pro High / Claude Opus)                  │
│  - Spawns agents      - Routes tasks     - Approves outputs     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  RESEARCHER   │  │  PRD SPECIALIST │  │  ARCHITECT    │
│ Gemini SERP   │  │  Claude Opus   │  │  Groq Llama   │
│ - Competitors │  │ - Requirements │  │ - Phased plans│
│ - Trends      │  │ - User stories │  │ - Technical   │
│ - Market data │  │ - Acceptance   │  │ - Roadmap     │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                ┌───────────────────────┐
                │    VALIDATOR          │
                │  - Cross-checks       │
                │  - Quality gates      │
                └───────────┬───────────┘
                            ▼
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   BUILDER      │  │   CI/CD AGENT │  │   DOCS AGENT  │
│   Groq Llama   │  │  Groq/GitHub │  │  Groq/Writer  │
│ - Code impl    │  │ - Pipeline   │  │ - README      │
│ - Components   │  │ - Tests      │  │ - Updates     │
│ - Features     │  │ - Deploy     │  │ - Templates   │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## Specialized Agents

### 1. Lead Orchestrator

**Model**: gemini/gemini-2-5-pro-exp-06-05 or anthropic/claude-opus-4-2025-06-20
**Role**: Central coordination, approval gates, agent spawning
**Skills**:

- Agent team spawning
- Task routing based on complexity
- Quality approval gates
- Budget management

### 2. Researcher Agent

**Model**: gemini/gemini-2-5-pro-exp-06-05 (SERP enabled)
**Role**: Market research, competitor analysis, trend identification
**Skills**:

- Google Search for real-time data
- SERP scraping and analysis
- Industry reports synthesis
- Data collection

**Commands**:

```
Research: "top marketing agencies Czech Republic 2026"
Research: "AI automation trends SMB 2026"
```

### 3. PRD Specialist Agent

**Model**: anthropic/claude-opus-4-2025-06-20
**Role**: Product Requirements, specifications, user stories
**Skills**:

- Requirements gathering
- User story creation
- Acceptance criteria
- Technical specifications

**Input**: Research data from Researcher
**Output**: `docs/prd-data/[project]-prd.md`

### 4. Roadmap Architect Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Phase planning, technical architecture, roadmap creation
**Skills**:

- BMAD phase planning
- Technical architecture
- Resource allocation
- Risk assessment

**Output**: `.agents/roadmap/phase-*.md`

### 5. Builder Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Code implementation, feature development
**Skills**:

- Full-stack development
- Component creation
- API integration
- Testing

**Trigger**: Phase 2+ approval

### 6. CI/CD Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Pipeline automation, deployment, infrastructure
**Skills**:

- GitHub Actions
- Vercel/Netlify deploy
- Docker/containers
- Monitoring setup

**Files Created**:

- `.github/workflows/*.yml`
- `Dockerfile`
- `docker-compose.yml`
- Deployment configs

### 7. Docs Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Documentation, README, progress updates
**Skills**:

- README generation
- API documentation
- Progress tracking
- Template creation

**Files Created**:

- `README.md` updates
- `docs/**/*.md`
- `CHANGELOG.md`
- Architecture diagrams

### 8. Progress Manager Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Track progress, update plans, manage blockers
**Skills**:

- Progress tracking
- Plan updates
- Blocker management
- Phase transitions

**Output**: `.agents/roadmap/progress.md` - auto-updated

### 9. Template Creator Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Create reusable templates for future projects
**Skills**:

- Template design
- Structure organization
- Documentation
- Version management

**Output**: `.agents/templates/**/*.md`

### 10. Validator Agent

**Model**: groq/llama-3.3-70b-versatile
**Role**: Quality gates, cross-checking, verification
**Skills**:

- Code review
- PRD validation
- Test coverage
- Security checks

---

## Cost Optimization Rules

| Task Type     | Model          | When to Use                |
| ------------- | -------------- | -------------------------- |
| Research/SERP | Gemini 3 Pro   | Daily free tier, real data |
| PRD/Strategy  | Claude Opus    | Complex reasoning, quality |
| Code/Impl     | Groq Llama 70B | 80% of tasks, fast/cheap   |
| Approval      | Claude Opus    | Final quality gates        |

**Budget Targets**:

- Groq: <$10/month (70B is cheap)
- Claude Opus: ~$15/month (10% of tasks)
- Gemini: Free tier (research only)

---

## Phased Workflow

### Phase 1: PRD & Research

**Duration**: 2-3 days
**Agents**: Researcher → PRD Specialist → Validator
**Models**: Gemini SERP → Claude Opus
**Output**:

- `docs/prd-data/research-summary.md`
- `docs/prd-data/[project]-prd.md`

### Phase 2: MVP Build

**Duration**: 5-7 days
**Agents**: Builder (parallel 2-3)
**Model**: Groq Llama 70B
**Output**:

- Working MVP
- Basic tests

### Phase 3: Measure

**Duration**: 3-5 days
**Agents**: Builder + Docs
**Model**: Groq Llama 70B
**Output**:

- Analytics integration
- A/B test setup

### Phase 4: Amplify

**Duration**: 5-7 days
**Agents**: Builder + CI/CD
**Model**: Groq Llama 70B
**Output**:

- SEO automation
- Ad integrations

### Phase 5: Deploy

**Duration**: 2-3 days
**Agents**: CI/CD + Docs
**Model**: Groq Llama 70B
**Output**:

- Production deployment
- Monitoring
- Documentation

### Phase 6: Templates & Scale

**Duration**: 2-3 days
**Agents**: Template Creator + Docs
**Model**: Groq Llama 70B
**Output**:

- Reusable templates
- Project structure

---

## Approval Gates

```
[Research] → [Inbox: Approve?] → [PRD] → [Inbox: Approve?] → [Build]
                                                              ↓
                                                         [Validate]
                                                              ↓
                                                    [Inbox: Approve?]
                                                              ↓
                                                       [Deploy/Release]
```

---

## File Structure

```
.agents/
├── roadmap/
│   ├── phase-1-prd.md
│   ├── phase-2-mvp.md
│   ├── phase-3-measure.md
│   ├── phase-4-amplify.md
│   ├── phase-5-deploy.md
│   └── progress.md          # Auto-updated
├── templates/
│   ├── prd/
│   │   ├── standard-prd.md
│   │   └── detailed-prd.md
│   ├── marketing-brief.md
│   └── README.md
└── agents/
    └── bmad-orchestrator.md
```

---

## Usage

### Start New Project

```
Lead Orchestrator: Create BMAD roadmap for [Project Name]
  1. Spawn Researcher → docs/prd-data/research-summary.md
  2. Spawn PRD Specialist → docs/prd-data/[project]-prd.md
  3. Spawn Roadmap Architect → .agents/roadmap/phase-*.md
  4. Await approval
```

### Update Progress

```
Progress Manager: Update phase progress
  - Check current phase status
  - Update .agents/roadmap/progress.md
  - Suggest next phase trigger
```

### Create Template

```
Template Creator: Create [Type] template
  - Use existing structure as reference
  - Save to .agents/templates/
  - Update .agents/templates/README.md
```
