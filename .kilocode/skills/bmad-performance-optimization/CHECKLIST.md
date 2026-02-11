# Performance Optimization Checklist

## Pre-Analysis
- [ ] Gather current performance metrics and baselines
- [ ] Review architecture diagrams and deployment topology
- [ ] Identify performance requirements (SLAs/SLOs, budgets, target response times)
- [ ] Collect observability data (metrics, traces, profiling dumps, load test reports)
- [ ] Validate instrumentation coverage

## Analysis Phase
- [ ] Analyze telemetry to pinpoint hotspots (CPU, memory, I/O, DB, network, frontend)
- [ ] Assess architecture decisions for scalability
- [ ] Identify caching opportunities
- [ ] Review database query patterns
- [ ] Analyze frontend paint times and bundle sizes

## Planning Phase
- [ ] Define performance goals and acceptance thresholds
- [ ] Create load/benchmark test plan
- [ ] Design optimization roadmap
- [ ] Prioritize optimizations by impact vs. effort
- [ ] Estimate capacity requirements

## Testing Phase
- [ ] Execute baseline performance tests
- [ ] Run load tests (normal, stress, soak, spike scenarios)
- [ ] Profile application under load
- [ ] Validate performance budgets
- [ ] Document regression safeguards

## Optimization Phase
- [ ] Implement code-level optimizations
- [ ] Optimize database queries and indexes
- [ ] Configure caching strategies
- [ ] Optimize CDN and asset delivery
- [ ] Tune infrastructure resources

## Verification Phase
- [ ] Re-run performance tests
- [ ] Compare before/after metrics
- [ ] Validate SLA/SLO compliance
- [ ] Update performance budgets
- [ ] Document lessons learned

## Documentation
- [ ] Create performance brief
- [ ] Document optimization backlog
- [ ] Update architecture diagrams
- [ ] Share findings with stakeholders
- [ ] Update monitoring dashboards
