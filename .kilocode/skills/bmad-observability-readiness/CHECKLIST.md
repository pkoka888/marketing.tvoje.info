# Observability Readiness Checklist

## Phase 1: Audit Current State

- [ ] **1.1** Inventory all existing telemetry tools (logging, metrics, tracing, APM)
- [ ] **1.2** Document current data collection coverage per service/component
- [ ] **1.3** Review existing metrics, logs, and traces for quality and completeness
- [ ] **1.4** Assess data retention policies and storage costs
- [ ] **1.5** Identify blind spots where issues have gone undetected
- [ ] **1.6** Review current dashboards and alerting configurations
- [ ] **1.7** Document on-call runbooks and escalation paths

## Phase 2: Define Objectives

- [ ] **2.1** Map user journeys and critical business workflows
- [ ] **2.2** Identify key performance indicators (KPIs) tied to business outcomes
- [ ] **2.3** Define Service Level Indicators (SLIs) for critical paths
- [ ] **2.4** Establish Service Level Objectives (SLOs) with error budgets
- [ ] **2.5** Align observability goals with incident response requirements
- [ ] **2.6** Document compliance and reporting requirements

## Phase 3: Design Instrumentation Strategy

- [ ] **3.1** Create metrics taxonomy (naming conventions, dimensions, units)
- [ ] **3.2** Define structured logging schema (fields, levels, sampling policies)
- [ ] **3.3** Design distributed tracing spans and context propagation
- [ ] **3.4** Specify events and semantic conventions for key operations
- [ ] **3.5** Define PII handling and data sanitization requirements
- [ ] **3.6** Document metric cardinality management strategy
- [ ] **3.7** Establish correlation between logs, metrics, and traces

## Phase 4: Alerting and On-Call

- [ ] **4.1** Design alerting strategy based on SLOs and error budgets
- [ ] **4.2** Define alert thresholds, severity levels, and escalation paths
- [ ] **4.3** Create runbooks for each alert type
- [ ] **4.4** Implement alert deduplication and noise reduction
- [ ] **4.5** Define on-call schedules and response time expectations
- [ ] **4.6** Document incident classification and communication templates

## Phase 5: Dashboards and Reporting

- [ ] **5.1** Design SLO dashboard with golden signals (latency, errors, traffic, saturation)
- [ ] **5.2** Create service-level dashboards for each critical component
- [ ] **5.3** Build business KPI dashboards aligned with objectives
- [ ] **5.4** Define data visualization standards and color conventions
- [ ] **5.5** Implement automated reporting for stakeholders
- [ ] **5.6** Set up cost monitoring for observability tooling

## Phase 6: Backlog and Implementation

- [ ] **6.1** Prioritize instrumentation gaps by business impact
- [ ] **6.2** Create implementation tasks with clear acceptance criteria
- [ ] **6.3** Assign owners and estimate effort for each task
- [ ] **6.4** Define testing approach for telemetry validation
- [ ] **6.5** Plan phased rollout with observability smoke tests
- [ ] **6.6** Schedule regular observability reviews and refinements

## Quality Gates

- [ ] Every critical user journey has metrics and alerts defined
- [ ] Logging standards specify structure, levels, and retention
- [ ] Alert runbooks documented or flagged for creation
- [ ] Dashboards provide actionable insights for on-call engineers
- [ ] PII and sensitive data handling complies with security policies
