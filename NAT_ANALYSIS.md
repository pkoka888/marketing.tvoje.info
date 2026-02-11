# NAT Port 2262 Analysis Report

## Problem Identified

Port 2262 is NOT accessible from external IP `89.203.173.196` despite being properly configured on server62.

## Root Cause Analysis

### ✅ Server62 Configuration (WORKING)

- **SSH Daemon**: Running and listening on ports 20 & 2262
- **Firewall**: UFW allows port 2262/tcp from anywhere
- **iptables**: ACCEPT rule for port 2262 configured
- **Network Interface**: ens18 with IP 192.168.1.62/24
- **Gateway**: 192.168.1.1 reachable (ping successful)

### ❌ External Connectivity Issue

- **External IP 89.203.173.196**: NOT reachable from server62
- **Traceroute**: All hops timeout (100% packet loss)
- **Ping**: 100% packet loss to external IP
- **NAT Forwarding**: Likely blocked at firewall/router level

## Network Architecture

```
Internet → Firewall (89.203.173.196) → NAT (2262→192.168.1.62:2262) → Server62
                ↓
            Server61 (Gateway/Traefik)
```

## Likely Culprits (in order of probability)

### 1. Firewall NAT Rules (MOST LIKELY)

- NAT forwarding rule for port 2262 may be missing or misconfigured
- Firewall may block port 2262 before NAT translation
- Interface binding issue on firewall

### 2. Router/Interface Configuration

- Port 2262 may be bound to wrong interface
- Firewall may have separate external vs internal interface rules
- NAT loopback prevention blocking internal access

### 3. ISP/Network Provider

- ISP may block certain port ranges
- External IP may be behind additional NAT

## Recommended Troubleshooting Steps

### Phase 1: Firewall Check

```bash
# On firewall/gateway (likely Server61)
sudo iptables -t nat -L -n | grep 2262
sudo iptables -L FORWARD -n | grep 2262
sudo ufw status verbose | grep 2262
```

### Phase 2: External Test

```bash
# From external network (not internal)
nmap -p 2262 89.203.173.196
telnet 89.203.173.196 2262
```

### Phase 3: Network Monitoring

```bash
# On firewall during connection attempt
sudo tcpdump -i any -n port 2262
sudo conntrack -L | grep 2262
```

## Temporary Workaround

- Use Tailscale VPN (working perfectly)
- Deploy via Server61 gateway
- Use internal network when on-site

## Fallback Deployment Strategy

### Primary: Tailscale VPN (✅ RECOMMENDED)

- **Connect**: `ssh s62ag` or `ssh s62`
- **Deployment**: Direct git clone/pull to `/var/www/marketing.tvoje.info/`
- **Advantages**: Secure, reliable, bypasses NAT issues

### Secondary: Server61 Gateway

- **Connect**: `ssh s61ag` then `ssh s62`
- **Deployment**: Proxy deployment through gateway
- **Use Case**: When Tailscale unavailable

### Tertiary: Direct NAT (NEEDS FIX)

- **Connect**: `ssh -p 2262 user@89.203.173.196`
- **Required**: Fix firewall NAT rules
- **Priority**: Low (Tailscale works perfectly)

## Next Actions

1. Fix NAT port 2262 on firewall (investigate Server61)
2. Document Tailscale as primary deployment method
3. Test deployment workflow via Tailscale
4. Configure GitHub Actions to use SSH key with agent user

## Current Status

- ✅ Tailscale VPN: WORKING
- ✅ Server62 SSH: WORKING
- ❌ NAT Port 2262: BLOCKED (firewall issue)
- ✅ Deployment environment: READY
