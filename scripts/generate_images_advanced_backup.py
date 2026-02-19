#!/usr/bin/env python3
"""
AI Image Generation Script
Supports multiple providers: Gemini, DALL-E, Stable Diffusion via Litellm

Usage:
    python scripts/generate_images_advanced.py --prompt "描述" --output output.png
    python scripts/generate_images_advanced.py --list-models
    python scripts/generate_images_advanced.py --batch prompts.txt
"""

import argparse
import base64
import os
import sys
import json
import requests
from pathlib import Path
from typing import Optional, List

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from google import genai
    GEMINI_AVAILABLE = True
    GEMINI_USES_NEW_API = True
except ImportError:
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
        GEMINI_USES_NEW_API = False
    except ImportError:
        GEMINI_AVAILABLE = False
        GEMINI_USES_NEW_API = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ImageGenerator:
    """Unified image generation across multiple providers."""
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        self._setup_providers()
    
    def _setup_providers(self):
        """Initialize provider clients."""
        # Gemini
        if GEMINI_AVAILABLE:
            gemini_key = os.environ.get("GEMINI_API_KEY")
            if gemini_key:
                if GEMINI_USES_NEW_API:
                    self.gemini_client = genai.Client(api_key=gemini_key)
                else:
                    genai.configure(api_key=gemini_key)
                print("✅ Gemini configured")
        
        # OpenAI DALL-E
        if OPENAI_AVAILABLE:
            openai_key = os.environ.get("OPENAI_API_KEY")
            if openai_key:
                self.openai_client = OpenAI(api_key=openai_key)
                print("✅ OpenAI configured")
        
        # LiteLLM proxy (for DALL-E, Stable Diffusion)
        litellm_url = os.environ.get("LITELLM_PROXY_URL", "http://localhost:4000")
        self.litellm_url = litellm_url
    
    def generate_gemini(self, prompt: str, output_path: str) -> bool:
        """Generate image using Gemini 2.0"""
        if not GEMINI_AVAILABLE:
            print("❌ Google GenerativeAI not installed")
            print("   pip install google-generativeai")
            return False
        
        try:
            if GEMINI_USES_NEW_API and hasattr(self, 'gemini_client'):
                # New google.genai API
                response = self.gemini_client.models.generate_images(
                    model='gemini-2.5-flash-image',
                    prompt=prompt,
                )
                # Handle new response format
                if hasattr(response, 'generated_images'):
                    image_data = response.generated_images[0].image.image_bytes
                else:
                    print("❌ Unexpected new API response format")
                    return False
            else:
                # Old google.generativeai API
                model = genai.GenerativeModel('gemini-2.5-flash-image')
                response = model.generate_content(prompt)
                
                # Handle different response formats
                if hasattr(response, 'image'):
                    image_data = response.image
                elif hasattr(response, 'parts'):
                    for part in response.parts:
                        if hasattr(part, 'image'):
                            image_data = part.image
                            break
                else:
                    print("❌ Unexpected response format")
                    return False
            
            # Save the image
            if isinstance(image_data, bytes):
                with open(output_path, 'wb') as f:
                    f.write(image_data)
            else:
                print(f"❌ Cannot save image - unexpected type: {type(image_data)}")
                return False
            
            print(f"✅ Saved: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return False
    
    def generate_dalle(self, prompt: str, output_path: str, model: str = "dall-e-3") -> bool:
        """Generate image using DALL-E via LiteLLM proxy or OpenAI directly."""
        if not OPENAI_AVAILABLE:
            print("❌ OpenAI not installed")
            print("   pip install openai")
            return False
        
        try:
            # Try LiteLLM first
            litellm_key = os.environ.get("LITELLM_API_KEY")
            if litellm_key:
                client = OpenAI(
                    api_key=litellm_key,
                    base_url=f"{self.litellm_url}/v1"
                )
                print(f"🔄 Using LiteLLM proxy: {self.litellm_url}")
            else:
                client = self.openai_client
                print("🔄 Using OpenAI directly")
            
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Download and save
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            print(f"✅ Saved: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ DALL-E error: {e}")
            return False
    
    def generate_stable_diffusion(self, prompt: str, output_path: str) -> bool:
        """Generate image using Stable Diffusion via LiteLLM."""
        try:
            # Using LiteLLM's image generation endpoint
            response = requests.post(
                f"{self.litellm_url}/v1/images/generations",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {os.environ.get('LITELLM_API_KEY', 'sk-dummy')}"
                },
                json={
                    "prompt": prompt,
                    "model": "stabilityai/stable-diffusion-xl-base-1.0",
                    "num_images": 1
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                image_url = data['data'][0]['url']
                img_data = requests.get(image_url).content
                
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"✅ Saved: {output_path}")
                return True
            else:
                print(f"❌ SD error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Stable Diffusion error: {e}")
            return False
    
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """Generate image using configured provider."""
        if self.provider == "gemini":
            return self.generate_gemini(prompt, output_path)
        elif self.provider == "dalle":
            return self.generate_dalle(prompt, output_path, kwargs.get("model", "dall-e-3"))
        elif self.provider == "sd":
            return self.generate_stable_diffusion(prompt, output_path)
        else:
            print(f"❌ Unknown provider: {self.provider}")
            return False


def list_models():
    """List available models from LiteLLM proxy."""
    print("\n📋 Available Image Generation Models")
    print("=" * 50)
    
    models = [
        ("gemini-2.5-flash-image", "Google Gemini 2.0 (Free daily)", "gemini"),
        ("dall-e-3", "OpenAI DALL-E 3 (Paid)", "dalle"),
        ("dall-e-2", "OpenAI DALL-E 2 (Paid)", "dalle"),
        ("stabilityai/stable-diffusion-xl", "Stable Diffusion XL (via LiteLLM)", "sd"),
    ]
    
    for model_id, desc, provider in models:
        print(f"  • {model_id}")
        print(f"    {desc}")
        print()


def batch_generate(prompts_file: str, output_dir: str, provider: str = "gemini"):
    """Generate images from a file of prompts."""
    prompts_path = Path(prompts_file)
    if not prompts_path.exists():
        print(f"❌ File not found: {prompts_file}")
        return
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    prompts = prompts_path.read_text().split('\n')
    prompts = [p.strip() for p in prompts if p.strip() and not p.startswith('#')]
    
    print(f"📝 Processing {len(prompts)} prompts...")
    
    gen = ImageGenerator(provider)
    
    for i, prompt in enumerate(prompts, 1):
        output_path = output_dir / f"image_{i:03d}.png"
        print(f"\n[{i}/{len(prompts)}] {prompt[:50]}...")
        gen.generate(prompt, str(output_path))


def main():
    parser = argparse.ArgumentParser(description="AI Image Generation Tool")
    parser.add_argument("--prompt", "-p", help="Image prompt")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--provider", default="gemini", 
                       choices=["gemini", "dalle", "sd"],
                       help="Provider to use")
    parser.add_argument("--model", "-m", default="dall-e-3",
                       help="Model name (for DALL-E)")
    parser.add_argument("--list-models", "-l", action="store_true",
                       help="List available models")
    parser.add_argument("--batch", "-b", help="Batch process prompts from file")
    parser.add_argument("--output-dir", default="output/images",
                       help="Output directory for batch")
    
    args = parser.parse_args()
    
    if args.list_models:
        list_models()
        return 0
    
    if args.batch:
        batch_generate(args.batch, args.output_dir, args.provider)
        return 0
    
    if not args.prompt or not args.output:
        parser.print_help()
        return 1
    
    gen = ImageGenerator(args.provider)
    success = gen.generate(args.prompt, args.output, model=args.model)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

