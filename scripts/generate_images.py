#!/usr/bin/env python3
"""Generate images using AI providers.

Providers:
  nvidia  — NVIDIA SDXL (free, default)
  openai  — DALL-E 3 (paid)

Usage:
    python scripts/generate_images.py \
        --prompt "..." --output path.png
    python scripts/generate_images.py \
        --prompt "..." --output path.png \
        --provider openai
"""

import os
import sys
import argparse
import base64

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_with_openai(prompt, output_file):
    """Generate image via DALL-E 3 (paid)."""
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found.")
            return False

        client = OpenAI(api_key=api_key)

        print(
            "Generating with DALL-E 3:"
            f" {prompt[:50]}..."
        )
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url",
        )

        image_url = response.data[0].url
        print(f"Downloading from {image_url[:50]}...")

        img_data = requests.get(
            image_url, timeout=60
        ).content
        with open(output_file, "wb") as f:
            f.write(img_data)
        print(f"Saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error generating with OpenAI: {e}")
        return False


def generate_with_nvidia(prompt, output_file):
    """Generate image via NVIDIA SDXL (free)."""
    try:
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            print("Error: NVIDIA_API_KEY not found.")
            return False

        url = (
            "https://ai.api.nvidia.com"
            "/v1/genai/stabilityai"
            "/stable-diffusion-xl"
        )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "NONE",
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        print(
            "Generating with NVIDIA SDXL:"
            f" {prompt[:50]}..."
        )
        response = requests.post(
            url, headers=headers,
            json=payload, timeout=120,
        )
        response.raise_for_status()
        body = response.json()

        artifacts = body.get("artifacts", [])
        if artifacts:
            b64 = artifacts[0]["base64"]
            img_data = base64.b64decode(b64)

            with open(output_file, "wb") as f:
                f.write(img_data)
            print(f"Saved to {output_file}")
            return True
        else:
            print(f"Unexpected response: {body}")
            return False

    except Exception as e:
        print(f"Error generating with NVIDIA: {e}")
        if hasattr(e, "response") and e.response:
            print(f"Response: {e.response.text}")
        return False


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate images using AI"
    )
    parser.add_argument(
        "--prompt", required=True,
        help="Image generation prompt",
    )
    parser.add_argument(
        "--output", required=True,
        help="Output file path (e.g. image.png)",
    )
    parser.add_argument(
        "--provider", default="nvidia",
        choices=["openai", "nvidia"],
        help="Provider (nvidia=free, openai=paid)",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    out = os.path.dirname(args.output)
    if out:
        os.makedirs(out, exist_ok=True)

    if args.provider == "openai":
        ok = generate_with_openai(
            args.prompt, args.output
        )
    else:
        ok = generate_with_nvidia(
            args.prompt, args.output
        )

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
