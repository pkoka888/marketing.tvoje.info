# Marketing.tvoje.info Deployment Fixes Plan

**Created:** 2026-02-19
**Status:** In Progress

---

## Issue 1: SSH Port 2262 Not Reachable

### Symptoms

- Direct SSH to s62 (192.168.1.62:2262) fails from public IP
- Connection timeout when trying port 2262 directly
- Previously working

### Investigation Steps

- [ ] Check iptables rules on s62
- [ ] Check UFW status and rules on s62
- [ ] Check fail2ban configurations
- [ ] Check sshd_config for IP restrictions
- [ ] Check network/firewall at ISP level
- [ ] Test with all protections disabled temporarily

### Potential Causes

1. ISP/router NAT not forwarding port 2262
2. iptables DROP rule on s62
3. UFW blocking port 2262
4. fail2ban banning connections
5. sshd_config AllowUsers/AllowGroups restrictions
6. Network ACL or cloud firewall

---

## Issue 2: Nginx Config on s60

### Problem

- `/etc/nginx/sites-available/marketing-static.conf` on s60 uses wrong SSL cert
- Uses `www.okamih.cz` instead of `marketing.tvoje.info`
- Traffic goes through s61 Traefik which has correct cert

### Fix

- [ ] Remove or disable the config on s60
- [ ] Verify no other conflicting configs

---

## Issue 3: Deployment Workflow

### Current State

- Deployment goes: GitHub → s60 → s62 (via internal SSH)
- Works correctly

### Recommended Cleanup

- [ ] Remove redundant nginx config on s60
- [ ] Ensure deployment documentation is up to date

---

## Investigation Commands

### Check SSH Access

```bash
# From local (Tailscale)
ssh sugent@s62  # via Tailscale

# Via jumphost
ssh -p 2260 sugent@89.203.173.196
ssh -p 2262 sugent@192.168.1.62

# Direct public (fails)
ssh -p 2262 sugent@89.203.173.196
```

### Check s62 Firewall

```bash
sudo iptables -L -n -v
sudo ufw status verbose
sudo fail2ban-client status
sudo systemctl status fail2ban
```

### Check SSH Config

```bash
sudo grep -E "AllowUsers|AllowGroups|DenyUsers|DenyGroups" /etc/ssh/sshd_config
sudo sshd -T | grep -E "allowusers|allowgroups|denyusers|denygroups"
```
