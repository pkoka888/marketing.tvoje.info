---
description: Node.js runtime environment considerations and best practices
globs: ["*.js", "*.ts", "*.mjs", "*.cjs"]
alwaysApply: false
---
# Node.js Runtime Guidelines

## Runtime Environment

### Version Requirements
- **Minimum Node.js Version**: 18.x LTS or higher
- **Package Manager**: npm (comes with Node.js) or pnpm
- **TypeScript Support**: Native ESM with `ts-node` or `tsx`

### Environment Variables
- `NODE_ENV`: Set to `development`, `production`, or `test`
- `PORT`: Server port (default: 3000)
- `DATABASE_URL`: Connection string for databases
- `API_KEY`: External service credentials

## Performance Considerations

### Memory Management
- Set `--max-old-space-size` for production (e.g., `--max-old-space-size=4096`)
- Monitor memory usage with `process.memoryUsage()`
- Enable garbage collection tuning for long-running processes

### CPU Utilization
- Use clustering for multi-core utilization
- Implement worker threads for CPU-intensive tasks
- Consider serverless for event-driven workloads

## Security Best Practices

### Dependency Management
- Use `npm audit` or `pnpm audit` regularly
- Enable lockfiles (`package-lock.json` or `pnpm-lock.yaml`)
- Use `npm ci` for reproducible builds

### Runtime Security
- Sanitize environment variables before use
- Validate all input with a schema validator (Zod, Yup)
- Set appropriate CSP headers
- Enable CORS with strict origin policies

## Error Handling

### Uncaught Exceptions
```javascript
process.on('uncaughtException', (error) => {
  // Log error with context
  logger.error('Uncaught exception:', error);
  // Perform graceful shutdown
  process.exit(1);
});
```

### Promise Rejections
```javascript
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled rejection at:', promise, 'reason:', reason);
});
```

## Logging

### Log Levels
| Level | Use Case |
|-------|----------|
| `error` | Application errors |
| `warn` | Warning conditions |
| `info` | Informational messages |
| `debug` | Debug information |
| `trace` | Detailed trace data |

### Best Practices
- Use structured JSON logging in production
- Include request IDs for traceability
- Avoid logging sensitive data
- Implement log rotation
