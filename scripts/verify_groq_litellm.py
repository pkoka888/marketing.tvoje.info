import os
import requests
import json

def verify_groq_litellm():
    """
    Verifies the connection to LiteLLM proxy and Groq using the specialized alias.
    """
    proxy_url = "http://localhost:4000/v1/chat/completions"
    model = "groq-fast-agent" # Use the new alias

    # Real task: Summarize our new .gitattributes
    with open(".gitattributes", "r") as f:
        git_attr_content = f.read()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a senior DevOps engineer."},
            {"role": "user", "content": f"Briefly explain the purpose of this .gitattributes file:\n\n{git_attr_content}"}
        ],
        "max_tokens": 100
    }

    print(f"--- Verifying Groq-Fast-Agent via LiteLLM ---")
    print(f"Proxy URL: {proxy_url}")
    print(f"Model Alias: {model}")

    try:
        response = requests.post(proxy_url, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"\nSuccess! Response from Groq:\n{content}")
        else:
            print(f"Error {response.status_code}: {response.text}")
            if "Authentication Error" in response.text or "API Key" in response.text:
                print("\nTIP: Make sure your GROQ_API_KEY is correctly set in the proxy environment.")
    except Exception as e:
        print(f"Connection failed: {e}")
        print("\nTIP: Ensure the LiteLLM proxy is running on port 4000.")

if __name__ == "__main__":
    verify_groq_litellm()
