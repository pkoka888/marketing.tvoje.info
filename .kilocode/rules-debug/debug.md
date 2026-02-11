---
description: Debug mode specific rules and troubleshooting guidelines
globs: ["*.ts", "*.js", "*.astro", "*.mdx"]
alwaysApply: false
---
# Debug Mode Rules

## Debug Mode Activation

### Environment Setup
- Set `DEBUG=true` or `NODE_ENV=development`
- Enable source maps in build configuration
- Configure verbose logging level

### VS Code Debugging
- Use `.vscode/launch.json` for debug configurations
- Set breakpoints in source files
- Use "Debug: Toggle Auto Attach" for automatic debugging

## Common Debugging Techniques

### 1. Console Logging
```typescript
// Use structured logging
logger.debug('Processing item', { itemId, status });

// Add context to errors
logger.error('Failed to process', { itemId, error: err.message });
```

### 2. Browser DevTools
- Use `console.log()`, `console.warn()`, `console.error()`
- Use `debugger;` statement for breakpoints
- Monitor Network tab for API calls
- Check Console for runtime errors

### 3. Astro Debugging
```bash
# Enable debug mode
npm run dev -- --debug

# View verbose output
DEBUG=* npm run dev
```

## TypeScript Debugging

### Common Issues
| Issue | Solution |
|-------|----------|
| Type errors | Run `npm run typecheck` |
| Import errors | Check path aliases in `tsconfig.json` |
| Runtime type errors | Add type guards |
| Module resolution | Check `baseUrl` and `paths` |

### Source Maps
- Ensure `sourceMap: true` in `tsconfig.json`
- Use `inlineSourceMap` for better error messages

## Astro-Specific Debugging

### Component Debugging
```astro
---
// Debug component props
console.log('Props received:', Astro.props);

// Debug slot content
console.log('Slots:', Object.keys(Astro.slots));
---
```

### API Route Debugging
```typescript
export const GET = async ({ request }) => {
  console.log('Request URL:', request.url);
  console.log('Request method:', request.method);
  
  // Debug response
  const response = await fetch(request.url);
  console.log('Response status:', response.status);
  
  return new Response(response.body);
};
```

## Common Issues & Solutions

### Build Issues
| Symptom | Solution |
|---------|----------|
| Memory errors | Increase Node.js heap size |
| Timeout errors | Increase build timeout |
| Module not found | Check imports and dependencies |
| TypeScript errors | Run `tsc --noEmit` |

### Runtime Issues
| Symptom | Solution |
|---------|----------|
| 404 errors | Check routing configuration |
| Hydration errors | Verify client directives |
| Style issues | Check Tailwind configuration |
| I18n issues | Verify translation files |

## Debugging Checklist

- [ ] Clear build cache: `npm run clean`
- [ ] Delete `node_modules/.astro`
- [ ] Restart dev server
- [ ] Check browser console for errors
- [ ] Verify environment variables
- [ ] Check network requests
- [ ] Validate component props
- [ ] Test in incognito mode
