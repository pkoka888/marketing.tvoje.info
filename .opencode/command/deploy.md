---
description: Deploy marketing site to production via Tailscale jumphost
subtask: true
---

Deploy the marketing site following the deployment workflow.

## Pre-deploy Checks

!`git status --short`
!`npm run build`

## Deployment Steps

Follow `.agent/workflows/deploy.md` exactly.

Key steps:
1. Build: `npm run build`
2. SSH via s60 jumphost (Tailscale): `ssh -J sugent@s60 sugent@s62`
3. Pull latest on server, restart container
4. Verify health endpoint responds

## Post-deploy

!`git log --oneline -5`

Report deployment status with server response confirmation.
