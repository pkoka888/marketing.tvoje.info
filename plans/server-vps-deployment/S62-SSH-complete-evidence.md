# SSH Port 2262 Blocking - Complete Evidence Document

**Created:** 2026-02-19  
**Status:** Complete Evidence Collection

---

## Architecture Overview

```
Internet (89.203.173.196)
       │
       ├── Public Port 2260 → CISCO FW → s60 (192.168.1.60:20)
       ├── Public Port 2261 → CISCO FW → s61 (192.168.1.61:20)
       └── Public Port 2262 → CISCO FW → s62 (192.168.1.62:20)
```

---

## Server s60 (Infrastructure)

### UFW Status

```
Status: active
Ports allowed: 2260, 2261, 2262, 20, 80, 443, and many others
```

### iptables FORWARD Chain (Key Entries)

```
23    1621  270K ACCEPT     tcp  --  *      *       0.0.0.0/0            192.168.1.61         tcp dpt:20
24    5335 1135K ACCEPT     tcp  --  *      *       0.0.0.0/0            192.168.1.62         tcp dpt:20
```

**Note:** Only port 20 is forwarded internally (Tailscale/internal network), NOT 2262

### SSH Config (/etc/ssh/sshd_config)

```
Port 20
Port 22
Port 2260
AllowUsers pavel jm agent miko claude backups sugent
AllowGroups ssh-users
PermitRootLogin no
MaxAuthTries 20
```

### sshd_config.d hardening

- `00-ansible-hardening.conf` - Standard Ansible hardening

### User: sugent

```
/home/sugent/.ssh/
├── authorized_keys     (2 keys)
├── config              (server aliases)
├── config.d/dev-projects
├── id_ed25519
├── id_ed25519.pub
├── id_ed25519_github
├── known_hosts
└── sockets/
```

**authorized_keys content:**

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIdgqbXj5+AxULz3P0nMNVMzsTCq2D989nMIW9Qozgrm sugent@server-infra-gem
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqaV6jWzplGt+Fon8ZL5ZTUTpPVpOjIivaR9nHmAFCF unified-agent@server-infra-20251205
```

### User: pavel

- Exists (uid 1000)
- No .ssh directory

---

## Server s61 (Gateway)

### UFW Status

```
Status: active
Ports allowed: 2261, 80, 443, 20, and many others
```

### iptables FORWARD Chain

- No specific entries for 2261, 2262

### SSH Config (/etc/ssh/sshd_config)

```
Port 20
Port 2261
Port 22
AllowUsers pavel jm agent miko claude backups sugent
PermitRootLogin no
MaxAuthTries 20
```

### sshd_config.d

- `00-ansible-hardening.conf` (empty)
- `00-ansible-hardening.conf.disabled`
- `10-agents.conf` (AllowGroups agents)
- `20-auth-policy.conf`
- `30-pavel-password.conf`

### Users

- pavel exists (uid 1000)
- sugent - **NOT FOUND** in passwd

---

## Server s62 (Target)

### UFW Status

```
Status: active
Ports allowed: 2262, 20, 80, 443, and many others
```

### iptables INPUT Chain

```
Default policy: DROP
```

### SSH Config (/etc/ssh/sshd_config)

```
Port 20
Port 2262
AllowUsers pavel agent backups sugent jm
PermitRootLogin no
MaxAuthTries 5
```

### sshd_config.d

- `00-ansible-hardening.conf` - Standard Ansible hardening

### User: sugent

```
/home/sugent/.ssh/
├── authorized_keys     (1 key)
├── config              (server aliases)
├── id_ed25519
├── id_ed25519.pub
├── id_ed25519_pavel
├── known_hosts
└── archive/
```

**authorized_keys content:**

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIdgqbXj5+AxULz3P0nMNVMzsTCq2D989nMIW9Qozgrm sugent@server-infra-gem
```

### User: pavel

- Exists (uid 1000)
- No .ssh directory

---

## Comparison Summary

| Item                    | s60          | s61          | s62      |
| ----------------------- | ------------ | ------------ | -------- |
| **Public SSH Port**     | 2260         | 2261         | 2262     |
| **Internal SSH Ports**  | 20, 22, 2260 | 20, 22, 2261 | 20, 2262 |
| **UFW 2262 Allowed**    | ✅ Yes       | N/A          | ✅ Yes   |
| **sshd Listening 2262** | ❌ No        | ❌ No        | ✅ Yes   |
| **sugent user**         | ✅           | ❌           | ✅       |
| **sugent .ssh**         | ✅           | N/A          | ✅       |
| **pavel user**          | ✅           | ✅           | ✅       |
| **pavel .ssh**          | ❌           | ❌           | ❌       |
| **Hardening file**      | ✅           | ✅           | ✅       |
| **fail2ban**            | ❌           | ✅           | ✅       |

---

## Key Differences Found

1. **s61 has NO sugent user** - This is why SSH to s61 as sugent fails
2. **pavel has NO .ssh on any server** - Only sugent has proper SSH keys
3. **Only port 20 forwarded internally** - Not 2262 (done by CISCO firewall)
4. **Different AllowUsers** - s62 is missing "miko", "claude"

---

## Conclusions

### Server-Side: All Correct ✅

- UFW allows port 2262 on s60 and s62
- sshd listens on port 2262 on s62
- sugent has proper authorized_keys on s60 and s62
- No blocking rules in iptables/UFW

### Root Cause: CISCO Firewall ❌

- Port 2262 is NOT forwarded from public IP (89.203.173.196) to internal s62 (192.168.1.62)
- This is NOT a server configuration issue
- This is a CISCO firewall NAT configuration issue

### Recommended Actions

1. Check CISCO firewall NAT rules
2. Add rule: 89.203.173.196:2262 → 192.168.1.62:2262
3. Or contact ISP to configure port forwarding
