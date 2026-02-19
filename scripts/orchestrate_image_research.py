#!/usr/bin/env python3
"""
Image Generation Deep Research V3
Extended research tasks for ComfyUI, resources, and LLM categories.

Usage:
    python scripts/orchestrate_image_research.py --list
"""

import sys

IMAGE_RESEARCH_TASKS = [
    {
        "agent": "bmad-comfyui-models",
        "description": "Research ComfyUI fine-tuned models",
        "priority": "HIGH",
        "prompt": """Research ComfyUI fine-tuned models and boilerplate.

1. Search for best ComfyUI models for marketing: portraits, logos, design
2. Look for LiteLLM integration with ComfyUI
3. Find ready-to-use workflows (boilerplate)
4. Document best models for each category
5. Save to plans/IMAGE_GENERATION_PLAN.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-comfyui-top2",
        "description": "Research top 2 ComfyUI implementations",
        "priority": "HIGH",
        "prompt": """Research the top 2 ComfyUI implementations for marketing images.

1. Find the best open source ComfyUI-based solutions
2. Check for pre-built workflows for: hero images, logos, social media
3. Look for API wrappers, LiteLLM integration
4. Document installation and usage
5. Save to docs/COMFYUI_TOP_IMPLEMENTATIONS.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-resource-needs",
        "description": "Research resource requirements",
        "priority": "MEDIUM",
        "prompt": """Research resource requirements for image generation LLMs.

1. VRAM needs for: SDXL, SD 1.5, FLUX, ComfyUI
2. RAM requirements
3. CPU vs GPU performance
4. Create a comparison table
5. Save to docs/IMAGE_LLM_RESOURCES.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-llm-categories",
        "description": "Research top LLMs by category",
        "priority": "HIGH",
        "prompt": """Research top 2026 image generation LLMs by category.

Create a compact reference with categories:
- Portrait/Photo
- Nature/Landscape
- Design/UI
- Artistic/Painting
- Vector/Illustration
- Logos/Branding

For each: best model, cost, quality rating
Save to docs/IMAGE_LLM_CATEGORIES.md

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    },
    {
        "agent": "bmad-agents-reference",
        "description": "Create agents.md reference",
        "priority": "HIGH",
        "prompt": """Create a compact reference for AGENTS.md.

1. Summarize all image generation options
2. Include: free/paid, quality, use case
3. Add commands for scripts
4. Create section for docs/IMAGE_AGENTS_REFERENCE.md
5. Include update frequency (when to refresh)

Use free model for research.""",
        "model": "x-ai/grok-code-fast-1:optimized:free"
    }
]


def list_tasks():
    print("\n🔬 Image Generation Deep Research (5 tasks)")
    print("=" * 60)
    for i, task in enumerate(IMAGE_RESEARCH_TASKS, 1):
        print(f"\n{i}. {task['description']}")
        print(f"   Agent: {task['agent']}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    
    if args.list:
        list_tasks()
        return 0
    
    print("🔬 Image Generation Deep Research V3\n")
    list_tasks()
    return 0


if __name__ == "__main__":
    sys.exit(main())
