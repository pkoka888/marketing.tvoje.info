# BMAD Story: S60 Production Deployment

# Story ID: DEPLOY-001

# Priority: HIGH

# Status: READY FOR IMPLEMENTATION

## Story

As a site owner, I need to deploy the marketing portfolio to S60 with Docker so
that the site is production-ready with AI tooling support.

## Business Value

- **Reliability**: S60 has 94GB RAM vs 3.8GB on S62 (25x more)
- **Direct Access**: Port 2260 is reachable (vs S62's blocked port 2262)
- **AI Integration**: MCP Gateway enables AI-powered development
- **Future-Proof**: Can host ComfyUI for image generation on S60

## Acceptance Criteria

- [ ] All 6 GitHub Secrets added
- [ ] Docker stack deployed on S60
- [ ] Redis container running
- [ ] MCP Gateway responding
- [ ] Nginx serving static files
- [ ] Site accessible at https://marketing.tvoje.info
- [ ] Automated deployment from main branch working

## Technical Requirements

### GitHub Secrets Required

```yaml
S60_HOST: '89.203.173.196'
S60_PORT: '2260'
S60_USER: 'sugent'
S60_SSH_KEY: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  [Your private key content]
  -----END OPENSSH PRIVATE KEY-----

REDIS_PASSWORD: '[32+ char random string]'
JWT_SECRET: '[64+ char random string]'
GITHUB_TOKEN: 'ghp_[...]'
FIRECRAWL_API_KEY: 'fc-[...]'
```

### Deployment Architecture

```
Internet → S60 Nginx → Static Files (dist/)
                ↓
           Docker Network (172.30.0.0/16)
                ↓
      ┌─────────┴─────────┐
      ↓                   ↓
   Redis:6379      MCP Gateway:3000
   (cache)         (7 MCP servers)
```

### Services

| Service     | Container            | Memory | Purpose                  |
| ----------- | -------------------- | ------ | ------------------------ |
| Redis       | marketing-redis      | 1G     | Session cache, MCP state |
| MCP Gateway | mcp-gateway          | 512M   | AI tool management       |
| Watchtower  | marketing-watchtower | 64M    | Auto-updates             |
| Nginx       | systemd              | 50M    | Web server               |

**Total:** ~1.6GB (of 94GB available)

## Implementation Steps

### Phase 1: Add Secrets (5 minutes)

```bash
# Generate strong passwords
openssl rand -base64 32  # REDIS_PASSWORD
openssl rand -base64 64  # JWT_SECRET

# Add to GitHub Secrets (via web UI or gh CLI)
gh secret set S60_HOST -b"89.203.173.196"
gh secret set S60_PORT -b"2260"
gh secret set S60_USER -b"sugent"
gh secret set S60_SSH_KEY < ~/.ssh/id_rsa_s60
gh secret set REDIS_PASSWORD -b"[generated]"
gh secret set JWT_SECRET -b"[generated]"
gh secret set GITHUB_TOKEN -b"ghp_..."
gh secret set FIRECRAWL_API_KEY -b"fc_..."
```

### Phase 2: Deploy (Automatic)

```bash
# Merge develop to main
git checkout main
git merge develop
git push origin main

# Monitor deployment
gh run watch
```

### Phase 3: Verify (2 minutes)

```bash
# SSH to S60
ssh -p 2260 sugent@89.203.173.196

# Check containers
cd /opt/marketing-docker
docker-compose -f docker-compose.prod.yml ps

# Test Redis
docker exec marketing-redis redis-cli -a [password] ping

# Test MCP Gateway
curl http://localhost:3000/health

# Test website
curl -I https://marketing.tvoje.info
```

## Rollback Plan

If deployment fails:

```bash
# On S60
cd /opt/marketing-docker
docker-compose -f docker-compose.prod.yml down

# Restore previous version from backup
sudo rsync -av /backup/marketing-previous/ /var/www/portfolio/
sudo nginx -s reload
```

## Monitoring

### Health Checks

- Redis: `docker exec marketing-redis redis-cli ping`
- MCP Gateway: `curl http://localhost:3000/health`
- Website: `curl -f https://marketing.tvoje.info`

### Logs

```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs -f

# View specific service
docker-compose -f docker-compose.prod.yml logs -f mcp-gateway
```

## Future Enhancements

### ComfyUI Self-Hosting (Phase 2)

S60's 94GB RAM is perfect for ComfyUI:

```yaml
# Add to docker-compose.prod.yml
comfyui:
  image: yanwk/comfyui-boot:cu121
  ports:
    - '8188:8188'
  volumes:
    - ./comfyui/models:/app/models
    - ./comfyui/output:/app/output
  deploy:
    resources:
      limits:
        memory: 16G
```

### LiteLLM Migration (Phase 2)

Move LiteLLM from S62 to S60:

- Update deploy-litellm.sh to target S60
- Use S60's better resources
- Unified deployment target

## Definition of Done

- [ ] All 6 secrets added to GitHub
- [ ] Workflow runs successfully
- [ ] All containers healthy
- [ ] Website accessible
- [ ] MCP Gateway functional
- [ ] Documentation updated
- [ ] Team notified

## Dependencies

- ✅ Docker configs ready
- ✅ Workflow file created
- ✅ S60 SSH tested (port 2260 open)
- ⏳ GitHub Secrets (6 required)

## Estimation

- **Secrets setup**: 5 minutes
- **Deployment**: 10 minutes (automated)
- **Verification**: 5 minutes
- **Total**: 20 minutes

## Risks

| Risk                | Mitigation                                 |
| ------------------- | ------------------------------------------ |
| S60 SSH key missing | Test: `ssh -p 2260 sugent@89.203.173.196`  |
| Secrets incorrect   | Verify in GitHub UI before deploy          |
| Docker not on S60   | Pre-check: `ssh s60 'docker --version'`    |
| Port conflicts      | Use non-standard ports (3000, 6379 mapped) |

## Notes

- S60 has 2.5TB disk - plenty of space
- S60 runs backups (borgmatic) - data is safe
- S60 is not the gateway (S61 is) - no Traefik complexity

---

**Next Action:** Add 6 GitHub Secrets, then push to main
