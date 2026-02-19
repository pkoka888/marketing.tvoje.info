import json

import requests


def search(q):
    url = f"https://registry.npmjs.org/-/v1/search?text={q}&size=5"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    for obj in data["objects"]:
        p = obj["package"]
        print(f"Name: {p['name']} | Desc: {p.get('description', '')}")


print("--- Playwright MCP Search ---")
search("playwright mcp")
