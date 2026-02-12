---
description: How to verify tool setup and agent environment at VSCode startup
---

# Verify Setup Workflow

// turbo-all

## Steps

1. Run the version check script:
```
python scripts/check-versions.py
```

2. Check that pre-commit hooks are installed:
```
python -m pre_commit --version
```

3. Verify Node.js matches .nvmrc:
```
node -v
```

4. Quick build test:
```
npm run build
```

5. Check that required MCP servers are available (if applicable):
```
docker ps
```
