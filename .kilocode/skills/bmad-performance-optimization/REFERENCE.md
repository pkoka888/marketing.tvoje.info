# Performance Optimization Reference

## Key Concepts

### Performance Budgets
- **Definition**: Pre-defined limits on resource sizes and load times
- **Types**: Bundle size, image size, API response time, total page weight
- **Tools**: Lighthouse, WebPageTest, Bundle Analyzer
- **Best Practice**: Set budgets early, enforce in CI/CD

### Core Web Vitals
- **LCP (Largest Contentful Paint)**: Time to render largest content element (<2.5s)
- **FID (First Input Delay)**: Time to first user interaction (<100ms)
- **CLS (Cumulative Layout Shift)**: Visual stability score (<0.1)
- **FCP (First Contentful Paint)**: First content rendered (<1.8s)
- **TTFB (Time to First Byte)**: Server response time (<600ms)

### Load Testing Patterns
- **Baseline**: Normal traffic patterns
- **Stress**: Beyond normal capacity to find breaking points
- **Soak**: Sustained load over time to detect memory leaks
- **Spike**: Sudden traffic increases to test auto-scaling

### Caching Strategies
- **Browser Cache**: Cache-Control headers for static assets
- **CDN Cache**: Edge caching for global distribution
- **Application Cache**: In-memory caching for frequent queries
- **Database Cache**: Query result caching (Redis, Memcached)
- **HTTP Cache**: ETag/Last-Modified for conditional requests

## Optimization Techniques

### Frontend
- **Code Splitting**: Load only needed JavaScript
- **Tree Shaking**: Remove unused code
- **Minification**: Remove whitespace and comments
- **Compression**: Gzip/Brotli for text assets
- **Lazy Loading**: Defer below-fold content
- **Image Optimization**: WebP/AVIF, responsive sizes
- **Font Optimization**: Subset, WOFF2 format
- **Critical CSS**: Inline above-fold styles

### Backend
- **Query Optimization**: Indexes, query rewriting, N+1 prevention
- **Connection Pooling**: Reuse database connections
- **Async Processing**: Offload heavy tasks to background jobs
- **Rate Limiting**: Protect against abuse
- **Pagination**: Limit result sets

### Infrastructure
- **Horizontal Scaling**: Add more instances
- **Vertical Scaling**: Increase instance size
- **Load Balancing**: Distribute traffic
- **Auto-scaling**: Scale based on metrics
- **Edge Computing**: Process closer to users

## Tools and Technologies

### Profiling
- **Chrome DevTools**: CPU, memory, network profiling
- **React Profiler**: Component render times
- **Node.js Profiler**: Event loop analysis
- **APM Tools**: Datadog, New Relic, Dynatrace

### Load Testing
- **k6**: Scriptable load testing
- **Locust**: Python-based load testing
- **Artillery**: Node.js load testing
- **JMeter**: Java-based load testing

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **ELK Stack**: Logs and metrics
- **CloudWatch**: AWS monitoring
- **Application Insights**: Azure monitoring

## Common Bottlenecks

### Database
- **Missing Indexes**: Full table scans
- **N+1 Queries**: Multiple queries for related data
- **Large Result Sets**: Fetching too much data
- **Connection Exhaustion**: Not pooling connections

### Network
- **High Latency**: Slow DNS, TCP handshake
- **Packet Loss**: Retransmissions
- **Bandwidth Saturation**: Network congestion
- **TLS Overhead**: SSL/TLS negotiation

### Application
- **Memory Leaks**: Unreleased references
- **Event Loop Blocking**: Synchronous operations
- **Garbage Collection**: Pauses from large allocations
- **Thread Contention**: Lock contention

## Performance Metrics

### Response Time Targets
- **P50**: Median response time
- **P95**: 95th percentile (SLA target)
- **P99**: 99th percentile (critical path)
- **P99.9**: 99.9th percentile (extreme cases)

### Throughput Metrics
- **RPS**: Requests per second
- **TPS**: Transactions per second
- **Concurrent Users**: Active sessions
- **Error Rate**: Failed requests percentage

### Resource Metrics
- **CPU Utilization**: Processing capacity
- **Memory Usage**: RAM consumption
- **Disk I/O**: Read/write operations
- **Network I/O**: Bandwidth usage

## Best Practices

### Measurement
- Measure early and often
- Use real user monitoring (RUM)
- Correlate metrics with business impact
- Establish baselines before optimization
- Track regressions automatically

### Optimization
- Optimize based on data, not assumptions
- Focus on high-impact, low-effort wins first
- Consider trade-offs (cost vs. performance)
- Document all changes and their impact
- Roll back if no improvement

### Architecture
- Design for performance from the start
- Use caching at every layer
- Make components independently scalable
- Plan for capacity growth
- Implement graceful degradation

## Resources

### Documentation
- [Web.dev Performance](https://web.dev/performance/)
- [MDN Performance](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [Google Lighthouse](https://github.com/GoogleChrome/lighthouse)

### Tools
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [WebPageTest](https://www.webpagetest.org/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Bundle Analyzer](https://webpack.js.org/analyse/)
