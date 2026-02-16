import socket
import ssl
import requests
import sys

def verify_site(hostname, port=443):
    print(f"--- Verifying {hostname}:{port} ---")

    # 1. DNS Check
    try:
        ip = socket.gethostbyname(hostname)
        print(f"[DNS] {hostname} -> {ip}")
    except Exception as e:
        print(f"[DNS] FAILED: {e}")
        return

    # 2. SSL/TLS Certificate Check
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                print(f"[SSL] Subject: {subject.get('commonName')}")
                print(f"[SSL] Issuer: {issuer.get('commonName')}")
                print(f"[SSL] Expiry: {cert['notAfter']}")
    except Exception as e:
        print(f"[SSL] FAILED: {e}")

    # 3. HTTP Response Check (Content Aware)
    try:
        url = f"https://{hostname}/"
        response = requests.get(url, timeout=10)
        print(f"[HTTP] Status: {response.status_code}")
        print(f"[HTTP] Server: {response.headers.get('Server')}")
        print(f"[HTTP] X-Debug-Origin: {response.headers.get('x-debug-origin')}")

        # Check for specific content or Astro indicators
        if "Astro" in response.text or "marketing" in response.text.lower():
            print("[HTTP] Content Match: SUCCESS (Astro indicators found)")
        else:
            print("[HTTP] Content Match: WARNING (No known indicators found)")

        if response.status_code != 200:
            print(f"[HTTP] Body snippet: {response.text[:200]}")
    except Exception as e:
        print(f"[HTTP] FAILED: {e}")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "marketing.tvoje.info"
    verify_site(host)
