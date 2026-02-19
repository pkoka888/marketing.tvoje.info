import io
import os
import tarfile

import requests


def download_and_extract(package_name, target_dir):
    print(f"📦 Fetching {package_name}...")
    try:
        # Get metadata
        res = requests.get(f"https://registry.npmjs.org/{package_name}", timeout=10)
        res.raise_for_status()
        data = res.json()
        latest_version = data["dist-tags"]["latest"]
        tarball_url = data["versions"][latest_version]["dist"]["tarball"]

        print(f"📥 Downloading version {latest_version} from {tarball_url}...")
        res = requests.get(tarball_url, timeout=30)
        res.raise_for_status()

        # Extract to target_dir
        os.makedirs(target_dir, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(res.content), mode="r:gz") as tar:
            tar.extractall(path=target_dir)

        print(f"✅ Successfully extracted to {target_dir}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    base_dir = ".kilocode/mcp-libs"
    os.makedirs(base_dir, exist_ok=True)

    # 1. Firecrawl
    download_and_extract("firecrawl-mcp", os.path.join(base_dir, "firecrawl"))

    # 2. Playwright
    download_and_extract("@playwright/mcp", os.path.join(base_dir, "playwright"))


if __name__ == "__main__":
    main()
