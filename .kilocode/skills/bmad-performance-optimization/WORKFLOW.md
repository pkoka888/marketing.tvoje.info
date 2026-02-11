# Performance Optimization Workflow

## Phase 1: Discovery & Analysis

### 1.1 Gather Requirements
- **Input**: User reports performance issues or requests optimization
- **Action**: Clarify performance goals, SLAs, and constraints
- **Output**: Performance requirements document

### 1.2 Collect Telemetry
- **Action**: Gather current metrics from monitoring tools
- **Sources**: APM dashboards, logs, profiling data, load test results
- **Check**: Instrumentation coverage with `bmad-observability-readiness`
- **Output**: Current performance baseline

### 1.3 Analyze Architecture
- **Action**: Review system architecture and deployment topology
- **Focus**: Identify scalability bottlenecks and optimization opportunities
- **Output**: Architecture assessment with recommendations

## Phase 2: Measurement & Profiling

### 2.1 Establish Baseline
- **Action**: Run comprehensive performance tests
- **Tests**: Lighthouse, load tests, profiling
- **Metrics**: LCP, FID, CLS, TTFB, throughput, error rates
- **Output**: Baseline performance report

### 2.2 Profile Under Load
- **Action**: Execute load testing scenarios
- **Scenarios**:
  - Baseline: Normal traffic patterns
  - Stress: 2-3x normal load
  - Soak: Sustained load over 1-2 hours
  - Spike: Sudden traffic surge
- **Output**: Load test results with bottleneck identification

### 2.3 Deep Profiling
- **Action**: Profile application at component level
- **Tools**: CPU profilers, memory profilers, database query analyzers
- **Focus**: Identify hotspots and resource contention
- **Output**: Profiling report with optimization targets

## Phase 3: Planning & Prioritization

### 3.1 Define Performance Budgets
- **Action**: Set measurable performance targets
- **Budgets**: Bundle size, API response time, page load time
- **Alignment**: Ensure budgets align with SLAs and business goals
- **Output**: Performance budget document

### 3.2 Create Optimization Roadmap
- **Action**: Prioritize optimizations by impact vs. effort
- **Framework**: Use RICE scoring (Reach, Impact, Confidence, Effort)
- **Categories**:
  - Quick wins (high impact, low effort)
  - Medium-term improvements
  - Long-term architectural changes
- **Output**: Prioritized optimization backlog

### 3.3 Design Test Strategy
- **Action**: Plan validation approach for each optimization
- **Tests**: A/B tests, canary deployments, feature flags
- **Success Criteria**: Measurable improvements with statistical significance
- **Output**: Test plan for each optimization

## Phase 4: Implementation

### 4.1 Execute Quick Wins
- **Action**: Implement high-impact, low-effort optimizations
- **Examples**:
  - Add missing database indexes
  - Enable compression
  - Optimize images
  - Cache frequently accessed data
- **Output**: Quick wins implemented and measured

### 4.2 Implement Medium-Term Improvements
- **Action**: Address medium-complexity bottlenecks
- **Examples**:
  - Refactor slow queries
  - Implement connection pooling
  - Add CDN caching
  - Optimize bundle size
- **Output**: Medium-term improvements deployed

### 4.3 Plan Long-Term Changes
- **Action**: Design architectural improvements for future iterations
- **Examples**:
  - Microservices decomposition
  - Event-driven architecture
  - Database sharding
  - Edge computing
- **Output**: Architectural roadmap

## Phase 5: Validation & Monitoring

### 5.1 Measure Impact
- **Action**: Re-run performance tests after each optimization
- **Compare**: Before/after metrics
- **Validate**: Against performance budgets and SLAs
- **Output**: Impact measurement report

### 5.2 Monitor in Production
- **Action**: Set up alerts and dashboards for key metrics
- **Alerts**: Performance regressions, SLA breaches, error rate spikes
- **Dashboards**: Real-time visibility into performance
- **Output**: Monitoring configuration

### 5.3 Document Learnings
- **Action**: Capture insights and best practices
- **Content**: What worked, what didn't, lessons learned
- **Share**: With team and update knowledge base
- **Output**: Post-optimization retrospective

## Phase 6: Continuous Improvement

### 6.1 Establish Performance Culture
- **Action**: Integrate performance into development workflow
- **Practices**:
  - Performance budgets in CI/CD
  - Automated regression testing
  - Performance code reviews
  - Regular capacity planning
- **Output**: Performance-first development process

### 6.2 Regular Reviews
- **Action**: Schedule periodic performance reviews
- **Frequency**: Monthly or quarterly depending on traffic growth
- **Activities**: Review metrics, identify new bottlenecks, plan optimizations
- **Output**: Continuous improvement cycle

## Handoff Points

### To `bmad-development-execution`
- When optimization implementation is ready
- Provide detailed implementation specifications
- Include acceptance criteria and measurement approach
- Coordinate testing and deployment

### To `bmad-observability-readiness`
- When instrumentation gaps are identified
- Request additional monitoring setup
- Define metrics and alerting requirements
- Validate telemetry coverage

### To `bmad-architecture-design`
- When architectural changes are needed
- Provide performance requirements and constraints
- Collaborate on scalable architecture design
- Review proposed changes for performance impact

## Success Criteria

- Performance budgets met or exceeded
- SLAs/SLOs consistently achieved
- Load tests pass all scenarios
- No performance regressions introduced
- Monitoring and alerting in place
- Team has performance improvement process
