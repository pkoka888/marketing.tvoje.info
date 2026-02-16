import sys
import os
import requests
import time

# Ensure we are running from the venv
print(f"Running verification from: {sys.executable}")

PROXY_URL = "http://localhost:4000/v1/chat/completions"
MODEL = "groq/llama-3.3-70b-versatile"

def wait_for_proxy(timeout=30):
    start = time.time()
    print("Waiting for proxy to perform health check...")
    while time.time() - start < timeout:
        try:
            # LiteLLM health endpoint
            requests.get("http://localhost:4000/health", timeout=1)
            print("Proxy is up!")
            return True
        except requests.exceptions.RequestException:
            time.sleep(1)
            print(".", end="", flush=True)
    print("\nProxy timed out.")
    return False

def verify_chat():
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": "Hello Groq!"}]
    }

    try:
        print(f"Sending request to {MODEL}...")
        response = requests.post(PROXY_URL, json=payload, timeout=20)
        if response.status_code == 200:
            print("Success! Groq replied:", response.json()['choices'][0]['message']['content'])
            return True
        else:
            print(f"Failed with {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    if wait_for_proxy():
        verify_chat()
    else:
        print("Skipping chat check as proxy is not reachable.")
