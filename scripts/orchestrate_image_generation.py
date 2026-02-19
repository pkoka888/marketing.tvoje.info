#!/usr/bin/env python3
"""
Image Generation Orchestrator V2
Extended research and implementation tasks.

Usage:
    python scripts/orchestrate_image_generation.py           # Run all tasks
    python scripts/orchestrate_image_generation.py --list     # List tasks only
"""

import sys
from pathlib import Path

# Image Generation Tasks for Subagents
IMAGE_GENERATION_TASKS = [
    {
        "agent": "bmad-gemini-fix",
        "description": "Fix Gemini API error and test",
        "priority": "HIGH",
        "prompt": """Fix the Gemini 2.0 image generation API error.

The current error is: "API key not valid. Please pass a valid API key."

1. Research the correct Gemini 2.0 image generation API model name for 2026
2. Check if the model name changed - try 'gemini-2.0-flash' or other variants
3. Update scripts/generate_images_advanced.py with correct model
4. Test again

Use free model x-ai/grok-code-fast-1:optimized:free for research and fix.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-comfyui-install",
        "description": "Research ComfyUI local installation",
        "priority": "HIGH",
        "prompt": """Research local ComfyUI installation for self-hosted image generation.

1. Check system requirements (GPU, RAM)
2. Research installation on Windows
3. Check if ComfyUI can be used via prompts/API
4. Create a simple installation guide in docs/
5. Document resource requirements

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-nvidia-image",
        "description": "Research NVIDIA image generation",
        "priority": "MEDIUM",
        "prompt": """Research NVIDIA AI image generation options.

1. Check if NVIDIA offers free image generation API
2. Research NVIDIA Nemo or other NVIDIA AI services
3. Look for free tiers or credits
4. Document findings in plans/IMAGE_GENERATION_PLAN.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-ollama-image",
        "description": "Research Ollama image generation",
        "priority": "MEDIUM",
        "prompt": """Research Ollama for image generation.

1. Can Ollama run image generation models locally?
2. What models are available (LLava, etc)?
3. What are the resource requirements (RAM, GPU)?
4. How to use it via API?
5. Document in plans/IMAGE_GENERATION_PLAN.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-free-alternatives",
        "description": "Research free image generation alternatives",
        "priority": "MEDIUM",
        "prompt": """Deep research: Find all free image generation options.

1. Search for "free image generation API no credit card"
2. Check HuggingFace Inference API free tier
3. Check Replicate free tier options
4. Check Cloudflare Workers AI free tier
5. Check Poe, Claude AI image features
6. Compile comprehensive list in plans/IMAGE_GENERATION_PLAN.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-litellm-update",
        "description": "Update LiteLLM for image generation",
        "priority": "LOW",
        "prompt": """Research and update LiteLLM for image generation.

1. Check litellm.ai/docs for image generation support
2. What providers are supported?
3. Any free providers?
4. Update scripts/generate_images_advanced.py if needed

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    }
]

VERIFICATION = [
    ("list-models", "python scripts/generate_images_advanced.py --list-models"),
    ("help", "python scripts/generate_images_advanced.py --help"),
]


def list_tasks():
    """List all tasks without executing."""
    print("\n🎨 Image Generation Tasks V2 (6 total)")
    print("=" * 60)
    for i, task in enumerate(IMAGE_GENERATION_TASKS, 1):
        priority = task["priority"]
        emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(priority, "⚪")
        print(f"\n{i}. {emoji} {task['description']} ({priority})")
        print(f"   Agent: {task['agent']}")
        print(f"   Model: {task['model']}")

    print("\n" + "=" * 60)
    print("📋 Verification (2 checks)")
    print("=" * 60)
    for name, cmd in VERIFICATION:
        print(f"  • {name}: {cmd}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Image Generation Orchestrator V2")
    parser.add_argument("--list", action="store_true", help="List tasks only")
    args = parser.parse_args()

    if args.list:
        list_tasks()
        return 0

    print("""
🎨 IMAGE GENERATION ORCHESTRATION V2

Extended research tasks:
1. Fix Gemini API error
2. ComfyUI local installation
3. NVIDIA image generation
4. Ollama image generation
5. Free alternatives deep research
6. LiteLLM image updates
""")
    list_tasks()

    return 0


if __name__ == "__main__":
    sys.exit(main())
