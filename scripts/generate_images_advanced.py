#!/usr/bin/env python3
"""AI Image Generation Script - Unified

Providers:
  nvidia   — NVIDIA SDXL (FREE, default)
  openai   — DALL-E 3 (paid)
  gemini   — Gemini 2.5 Flash Image (FREE daily)
  cloudflare — Cloudflare Workers AI (FREE)

Usage:
    python scripts/generate_images_advanced.py --prompt "..." --output image.png
    python scripts/generate_images_advanced.py --prompt "..." --output image.png --provider nvidia
    python scripts/generate_images_advanced.py --list-models
"""

import os
import sys
import argparse
import base64

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_with_nvidia(prompt, output_file):
    """Generate image via NVIDIA SDXL (FREE - 1000-5000 credits)."""
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

        print(f"Generating with NVIDIA SDXL: {prompt[:50]}...")
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
            print(f"✅ Saved to {output_file}")
            return True
        else:
            print(f"❌ Unexpected response: {body}")
            return False

    except Exception as e:
        print(f"❌ Error generating with NVIDIA: {e}")
        return False


def generate_with_openai(prompt, output_file):
    """Generate image via DALL-E 3 (paid)."""
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found.")
            return False

        client = OpenAI(api_key=api_key)

        print(f"Generating with DALL-E 3: {prompt[:50]}...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url",
        )

        image_url = response.data[0].url
        img_data = requests.get(image_url, timeout=60).content
        with open(output_file, "wb") as f:
            f.write(img_data)
        print(f"✅ Saved to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error generating with OpenAI: {e}")
        return False


def generate_with_gemini(prompt, output_file):
    """Generate image via Gemini 2.5 Flash Image (FREE daily)."""
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found.")
            return False

        client = genai.Client(api_key=api_key)

        print(f"Generating with Gemini 2.5 Flash: {prompt[:50]}...")
        response = client.models.generate_images(
            model='gemini-2.5-flash-image',
            prompt=prompt,
        )

        if hasattr(response, 'generated_images'):
            image_data = response.generated_images[0].image.image_bytes
            with open(output_file, "wb") as f:
                f.write(image_data)
            print(f"✅ Saved to {output_file}")
            return True
        else:
            print(f"❌ Unexpected response format")
            return False

    except Exception as e:
        print(f"❌ Error generating with Gemini: {e}")
        return False


def generate_with_cloudflare(prompt, output_file):
    """Generate image via Cloudflare Workers AI (FREE - 10k neurons/day)."""
    try:
        # Cloudflare Workers AI with FLUX model
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        api_token = os.getenv("CLOUDFLARE_API_TOKEN")

        if not account_id or not api_token:
            print("Error: CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN required.")
            return False

        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"

        headers = {
            "Authorization": f"Bearer {api_token}",
        }

        payload = {
            "prompt": prompt,
        }

        print(f"Generating with Cloudflare FLUX: {prompt[:50]}...")
        response = requests.post(
            url, headers=headers,
            json=payload, timeout=120,
        )

        if response.status_code == 200:
            data = response.json()
            if 'images' in data:
                import base64
                b64 = data['images'][0]['base64']
                img_data = base64.b64decode(b64)
                with open(output_file, "wb") as f:
                    f.write(img_data)
                print(f"✅ Saved to {output_file}")
                return True

        print(f"❌ Cloudflare error: {response.status_code} - {response.text}")
        return False

    except Exception as e:
        print(f"❌ Error generating with Cloudflare: {e}")
        return False


def list_models():
    """List available models."""
    print("\n📋 Available Image Generation Models")
    print("=" * 50)
    print("  • nvidia (FREE)      - NVIDIA SDXL (1000-5000 credits)")
    print("  • gemini (FREE)      - Gemini 2.5 Flash Image (daily)")
    print("  • cloudflare (FREE)  - Cloudflare FLUX (10k/day)")
    print("  • openai (PAID)      - DALL-E 3")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="AI Image Generation - Unified Script"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="Image generation prompt",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path",
    )
    parser.add_argument(
        "--provider", default="nvidia",
        choices=["nvidia", "openai", "gemini", "cloudflare"],
        help="Provider (default: nvidia)",
    )
    parser.add_argument(
        "--list-models", "-l",
        action="store_true",
        help="List available models",
    )

    args = parser.parse_args()

    if args.list_models:
        list_models()
        return 0

    if not args.prompt or not args.output:
        parser.print_help()
        return 1

    # Ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    if args.provider == "nvidia":
        ok = generate_with_nvidia(args.prompt, args.output)
    elif args.provider == "openai":
        ok = generate_with_openai(args.prompt, args.output)
    elif args.provider == "gemini":
        ok = generate_with_gemini(args.prompt, args.output)
    elif args.provider == "cloudflare":
        ok = generate_with_cloudflare(args.prompt, args.output)
    else:
        print(f"❌ Unknown provider: {args.provider}")
        ok = False

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
