# Architecture Design Reference

## Key Concepts

- **Decision Architecture**: A structured document that captures architectural decisions, rationale, and trade-offs for a system.
- **Architecture Drivers**: Quality attributes (performance, security, scalability, maintainability) and constraints that shape design choices.
- **Component Topology**: The arrangement and relationships of system components, including data flows and integration points.
- **Tech Stack Rationale**: The justification for selecting specific technologies, frameworks, and tools.

## Best Practices

- **Traceability**: Every architectural decision should be traceable to a requirement, constraint, or quality attribute.
- **Alternatives Analysis**: Document at least 2-3 alternatives for major decisions, with pros/cons.
- **Risk Mitigation**: Identify potential risks and mitigation strategies for each major decision.
- **Implementation Guardrails**: Provide clear guidelines and constraints for implementation teams.

## Common Patterns

- **Layered Architecture**: Separation of concerns into presentation, business logic, and data layers.
- **Microservices**: Decomposition into independent, loosely-coupled services.
- **Event-Driven**: Asynchronous communication via events/messages.
- **CQRS**: Command Query Responsibility Segregation for read/write separation.

## Decision Framework

1. **Identify Drivers**: What are the key quality attributes and constraints?
2. **Generate Alternatives**: What are the viable options?
3. **Evaluate**: Compare alternatives against drivers.
4. **Select**: Choose the best option with rationale.
5. **Document**: Record decision, rationale, and trade-offs.

## Resources

- **Software Architecture in Practice** by Len Bass et al.
- **Building Evolutionary Architectures** by Neal Ford
- **AWS Well-Architected Framework**
- **12-Factor App** methodology
- **Clean Architecture** by Robert C. Martin
