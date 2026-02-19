# BMAD Research: SSH Port Blocking Investigation

**Project:** Server Infrastructure SSH Access Analysis **Type:**
DevOps/Infrastructure Research **Level:** 2 (Medium - Multi-server
investigation) **Created:** 2026-02-19

---

## Problem Statement

SSH connection to port 2262 on server s62 (192.168.1.62) fails with timeout when
accessed directly via public IP (89.203.173.196:2262), but works via jumphost
(s60 → s62).

**Objective:** Identify ALL possible locations on Debian/Linux that can block
SSH access to a specific port.

---

## Research Categories

### 1. Network Level (ISP/Router)

| Location                   | Config File   | Commands to Check           |
| -------------------------- | ------------- | --------------------------- |
| ISP Router NAT             | Web UI        | Check port forwarding rules |
| Routerptables/nft Firewall | iables        | `iptables -L -n -v`         |
| Cloud Firewall             | Provider UI   | Check security groups       |
| Port Forwarding            | Router config | Verify 2262 → 192.168.1.62  |

**Evidence needed:**

- Router NAT table
- Port forwarding rules
- Firewall logs

---

### 2. Host Firewall (iptables)

| Chain       | Purpose           | Key Commands                           |
| ----------- | ----------------- | -------------------------------------- |
| INPUT       | Incoming packets  | `iptables -L INPUT -n -v`              |
| FORWARD     | Forwarded packets | `iptables -L FORWARD -n -v`            |
| OUTPUT      | Outgoing packets  | `iptables -L OUTPUT -n -v`             |
| PREROUTING  | NAT prerouting    | `iptables -t nat -L PREROUTING -n -v`  |
| POSTROUTING | NAT postrouting   | `iptables -t nat -L POSTROUTING -n -v` |

**Key checks:**

- DROP/REJECT rules on port 2262
- CONNTRACK connection states
- Recent packet counters showing drops

**Evidence needed:**

- Full iptables OUTPUT (all chains)
- NAT table (PREROUTING, POSTROUTING)
- Recent log entries with packet drops

---

### 3. UFW (Uncomplicated Firewall)

| Command              | Purpose            |
| -------------------- | ------------------ |
| `ufw status verbose` | List all rules     |
| `ufw show added`     | Show added rules   |
| `ufw show raw`       | Raw iptables rules |
| `/etc/ufw/*.rules`   | Rule files         |
| `/etc/ufw/ufw.conf`  | Main config        |
| `/etc/default/ufw`   | Default policies   |

**Key checks:**

- Port 2262 explicitly denied
- Default input policy DROP/REJECT
- UFW enabled but not running

**Evidence needed:**

- Full `ufw status verbose` output
- All files in `/etc/ufw/`
- UFW logs in `/var/log/ufw*`

---

### 4. fail2ban

| File/Location                    | Purpose            |
| -------------------------------- | ------------------ |
| `/etc/fail2ban/jail.local`       | Custom jail config |
| `/etc/fail2ban/jail.d/`          | Jail overrides     |
| `/var/log/fail2ban.log`          | Fail2ban logs      |
| `fail2ban-client status`         | Active jails       |
| `fail2ban-client get sshd banip` | Banned IPs         |

**Key checks:**

- sshd jail banning our IP
- Custom port in jail config
- Bantime/retry settings
- Regex matching our connection attempts

**Evidence needed:**

- All jail configurations
- Fail2ban logs (last 1000 lines)
- Current banned IPs
- Fail2ban regex tests

---

### 5. SSH Daemon (sshd)

| File                            | Purpose         |
| ------------------------------- | --------------- |
| `/etc/ssh/sshd_config`          | Main config     |
| `/etc/ssh/sshd_config.d/*.conf` | Include files   |
| `/var/log/auth.log`             | SSH auth logs   |
| `ss -tlnp \| grep sshd`         | Listening ports |

**Key checks:**

- `Port` directive (multiple ports?)
- `ListenAddress` restrictions
- `AllowUsers` / `AllowGroups`
- `DenyUsers` / `DenyGroups`
- `MaxAuthTries` limits
- `ClientAliveInterval` timeouts
- `PermitRootLogin` setting
- `PasswordAuthentication` vs `PubkeyAuthentication`
- `Match` blocks with IP restrictions

**Evidence needed:**

- Full sshd_config with all includes
- All files in sshd_config.d/
- Recent auth.log entries for SSH
- ss/netstat output for port 2262

---

### 6. User/Group Permissions

| File              | Purpose            |
| ----------------- | ------------------ |
| `/etc/passwd`     | User accounts      |
| `/etc/group`      | Group memberships  |
| `/etc/sudoers`    | Sudo permissions   |
| `/etc/sudoers.d/` | Sudo include files |

**Key checks:**

- User exists and has shell
- Group membership allows SSH
- Sudo rules not blocking

**Evidence needed:**

- passwd entry for user
- group entries for user
- sudoers files

---

### 7. SELinux / AppArmor

| System   | Commands                                       |
| -------- | ---------------------------------------------- |
| SELinux  | `getenforce`, `sestatus`, `semodule -l`        |
| AppArmor | `aa-status`, `aa-complain`, `/etc/apparmor.d/` |

**Key checks:**

- SELinux enforcing blocking port
- AppArmor profile blocking SSH

**Evidence needed:**

- SELinux status
- AppArmor status
- Relevant profiles

---

### 8. System Limits

| File                        | Purpose        |
| --------------------------- | -------------- |
| `/etc/security/limits.conf` | PAM limits     |
| `/etc/pam.d/*`              | PAM config     |
| `/proc/sys/net/core/`       | Network limits |

**Key checks:**

- Max user processes
- Max open files
- Network buffer limits

**Evidence needed:**

- limits.conf
- relevant PAM configs

---

### 9. Network Configuration

| Command                | Purpose       |
| ---------------------- | ------------- |
| `ip addr`              | IP addresses  |
| `ip route`             | Routing table |
| `ip neigh`             | ARP table     |
| `cat /etc/resolv.conf` | DNS config    |
| `/etc/hosts`           | Host file     |

**Key checks:**

- Interface up on correct network
- Route to source IP exists
- No blackhole routes

**Evidence needed:**

- Full ip addr output
- Full ip route output
- ARP table

---

### 10. Docker Network

| Command                  | Purpose         |
| ------------------------ | --------------- |
| `docker network ls`      | Docker networks |
| `docker network inspect` | Network details |
| `iptables -L DOCKER`     | Docker iptables |

**Key checks:**

- Docker bridge conflicting
- Docker userland proxy issues

**Evidence needed:**

- Docker network list
- DOCKER chain in iptables

---

### 11. Cloud Provider (if applicable)

| Provider     | Check                  |
| ------------ | ---------------------- |
| AWS          | Security Groups, NACLs |
| GCP          | Firewall rules         |
| Azure        | NSGs                   |
| DigitalOcean | Cloud Firewall         |

**Evidence needed:**

- Provider firewall rules UI screenshot

---

### 12. DNS/Reverse DNS

| Check         | Command                   |
| ------------- | ------------------------- |
| Forward DNS   | `nslookup 89.203.173.196` |
| Reverse DNS   | `dig -x 89.203.173.196`   |
| RDNS mismatch | Compare with hostname     |

---

### 13. TCP Wrappers

| File               | Purpose       |
| ------------------ | ------------- |
| `/etc/hosts.allow` | Allowed hosts |
| `/etc/hosts.deny`  | Denied hosts  |

**Key checks:**

- sshd in hosts.allow/deny
- IP/hostname restrictions

**Evidence needed:**

- Both files content

---

### 14. Network Namespaces

| Command                  | Purpose              |
| ------------------------ | -------------------- |
| `ip netns list`          | List namespaces      |
| `ip netns exec <ns> ...` | Execute in namespace |

**Key checks:**

- SSH in different namespace

---

### 15. SystemD Services

| Command                 | Purpose             |
| ----------------------- | ------------------- |
| `systemctl status ssh`  | SSH service status  |
| `systemctl status sshd` | sshd service status |
| `journalctl -u ssh`     | SSH logs            |

**Key checks:**

- Service running
- Service enabled
- Recent restarts/failures

**Evidence needed:**

- Full systemctl status
- Recent journalctl for ssh

---

## Evidence Collection Checklist

### Server s60 (Infrastructure)

- [ ] `sudo iptables -L -n -v --line-numbers`
- [ ] `sudo iptables -t nat -L -n -v`
- [ ] `sudo ufw status verbose`
- [ ] `sudo ufw status numbered`
- [ ] `cat /etc/ufw/ufw.conf`
- [ ] `cat /etc/ufw/default*.rules`
- [ ] `sudo ss -tlnp | grep 226`
- [ ] `sudo fail2ban-client status`
- [ ] `sudo fail2ban-client get sshd banip`
- [ ] `sudo cat /var/log/fail2ban.log | tail -500`
- [ ] `sudo ip route`
- [ ] `sudo ip addr`
- [ ] `sudo iptables -L FORWARD -n -v`

### Server s61 (Gateway)

- [ ] `sudo iptables -L -n -v --line-numbers`
- [ ] `sudo iptables -t nat -L -n -v`
- [ ] `sudo ufw status verbose`
- [ ] `sudo ss -tlnp | grep 226`
- [ ] Router NAT forwarding screenshot

### Server s62 (Target)

- [ ] `sudo iptables -L INPUT -n -v --line-numbers`
- [ ] `sudo iptables -L FORWARD -n -v --line-numbers`
- [ ] `sudo ufw status verbose`
- [ ] `sudo ufw status numbered`
- [ ] `sudo cat /etc/ssh/sshd_config`
- [ ] `sudo ls -la /etc/ssh/sshd_config.d/`
- [ ] `sudo cat /etc/ssh/sshd_config.d/*`
- [ ] `sudo ss -tlnp | grep 2262`
- [ ] `sudo fail2ban-client status`
- [ ] `sudo fail2ban-client get sshd banip`
- [ ] `sudo tail -500 /var/log/fail2ban.log`
- [ ] `sudo tail -500 /var/log/auth.log | grep ssh`
- [ ] `sudo systemctl status sshd`
- [ ] `sudo getenforce` (if SELinux)
- [ ] `sudo aa-status`
- [ ] `sudo ip route`
- [ ] `sudo ip addr`
- [ ] `sudo docker network ls`

### Local (Client)

- [ ] `nslookup 89.203.173.196`
- [ ] `dig -x 89.203.173.196`
- [ ] `traceroute 89.203.173.196` or `mtr 89.203.173.196`
- [ ] SSH with -vvv debug output

---

## Research Notes

### Known Working Paths

- Tailscale: `ssh sugent@100.91.164.109 -p 20` ✅ Works
- Internal: `ssh sugent@192.168.1.62 -p 2262` ✅ Works
- Via s60: `ssh -p 2260 sugent@89.203.173.196` →
  `ssh -p 2262 sugent@192.168.1.62` ✅ Works

### Failing Path

- Direct public: `ssh -p 2262 sugent@89.203.173.196` ❌ Timeout

### Hypothesis

Port 2262 is NOT forwarded at ISP router/NAT level to internal IP 192.168.1.62.
This is NOT a server-side issue.

---

## CORRECT Architecture

```
Internet → CISCO Firewall (NAT) → Internal Network 192.168.1.0/24
                                    ├── s60 (192.168.1.60) - Public:2260 → Internal:20
                                    ├── s61 (192.168.1.61) - Public:2261 → Internal:20
                                    └── s62 (192.168.1.62) - Public:2262 → Internal:20
```

**Note:** CISCO firewall handles public→internal port mapping. Servers listen on
internal port 20 (or custom like 2260, 2262 on s60 itself).

---

## Evidence Collected (2026-02-19)

### SSH Config Comparison

| Server  | Ports Configured  | AllowUsers                                      | AllowGroups | Hardening File                                                                         |
| ------- | ----------------- | ----------------------------------------------- | ----------- | -------------------------------------------------------------------------------------- |
| **s60** | Port 20, 22, 2260 | pavel, jm, agent, miko, claude, backups, sugent | ssh-users   | 00-ansible-hardening.conf                                                              |
| **s61** | Port 20, 22, 2261 | pavel, jm, agent, miko, claude, backups, sugent | (none)      | 00-ansible-hardening.conf, 10-agents.conf, 20-auth-policy.conf, 30-pavel-password.conf |
| **s62** | Port 20, 2262     | pavel, agent, backups, sugent, jm               | (none)      | 00-ansible-hardening.conf                                                              |

### s60 SSH Config Details:

```
Port 20
Port 22
Port 2260
AllowUsers pavel jm agent miko claude backups sugent
AllowGroups ssh-users
PermitRootLogin no
MaxAuthTries 20
PubkeyAuthentication yes
PasswordAuthentication yes
AllowTcpForwarding yes
```

### s61 SSH Config Details:

```
Port 20
Port 2261
Port 22
AllowUsers pavel jm agent miko claude backups sugent
MaxAuthTries 20
PermitRootLogin no
UseDNS no
PubkeyAuthentication yes
PasswordAuthentication yes
```

### s62 SSH Config Details:

```
Port 20
Port 2262
AllowUsers pavel agent backups sugent jm
MaxAuthTries 5
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication yes
```

### Firewall Status

| Server | UFW Status | Port 2262 Allowed  | fail2ban               |
| ------ | ---------- | ------------------ | ---------------------- |
| s60    | Active     | ✅ Yes (IPv4+IPv6) | Not installed          |
| s61    | Active     | N/A                | ✅ Running (sshd jail) |
| s62    | Active     | ✅ Yes (IPv4+IPv6) | ✅ Running (sshd jail) |

### s60 Listening Ports:

- Port 20 (SSH - internal)
- Port 22 (SSH - internal)
- Port 2260 (SSH - public access on s60 itself)

### s62 Listening Ports:

- Port 20 (SSH - internal)
- Port 2262 (SSH - should be accessible via public IP:2262)

### Conclusion

**The issue is at CISCO firewall level** - port 2262 is not forwarded from
public IP to internal s62. This is NOT a server config issue - it's a missing
NAT port forwarding rule on CISCO firewall.

All server-side configurations are correct:

- ✅ UFW allows port 2262
- ✅ sshd listens on port 2262
- ✅ AllowUsers includes sugent
- ✅ No fail2ban bans

---

## Next Steps

1. **Collect evidence** using checklist above
2. **Analyze each category** for blocking rules
3. **Document findings** with timestamps
4. **Verify hypothesis** about ISP-level blocking
