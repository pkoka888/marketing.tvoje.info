#!/usr/bin/env python3
"""
Agent Tools - Standardized LiteLLM/Groq Interface

This library provides a unified interface for agents to call Groq via LiteLLM.

Usage:
    from agent_tools import ask_groq, analyze_code, research_task

    # Simple query
    result = ask_groq("What is the capital of Czech Republic?")

    # Code analysis
    result = analyze_code("path/to/file.py")

    # Research task
    result = research_task("marketing agencies Czech Republic")
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configuration
LITELLM_URL = os.getenv("LITELLM_PROXY_URL", "http://localhost:4000")
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-local-dev-1234")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model routing
MODELS = {
    "fast": "groq/llama-3.1-8b-instant",
    "balanced": "groq/mixtral-8x7b-32768",
    "smart": "groq/llama-3.3-70b-versatile",
    "reasoning": "groq/llama-3.1-70b-versatile",
    "flash": "gemini-flash",
    "pro": "gemini-pro",
}


@dataclass
class AgentResponse:
    """Standardized response format"""

    success: bool
    content: str
    model: str
    tokens_used: int
    duration_ms: int
    error: Optional[str] = None


class LiteLLMClient:
    """Client for LiteLLM proxy"""

    def __init__(self, base_url: str = LITELLM_URL, api_key: str = LITELLM_MASTER_KEY):
        self.base_url = base_url
        self.api_key = api_key

    def complete(
        self,
        prompt: str,
        model: str = "groq/llama-3.3-70b-versatile",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AgentResponse:
        """Make a completion request"""
        import time

        import requests

        start_time = time.time()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

            duration_ms = int((time.time() - start_time) * 1000)

            return AgentResponse(
                success=True,
                content=data["choices"][0]["message"]["content"],
                model=data.get("model", model),
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                duration_ms=duration_ms,
            )
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentResponse(
                success=False,
                content="",
                model=model,
                tokens_used=0,
                duration_ms=duration_ms,
                error=str(e),
            )


# Global client instance
_client: Optional[LiteLLMClient] = None


def get_client() -> LiteLLMClient:
    """Get or create the global client"""
    global _client
    if _client is None:
        _client = LiteLLMClient()
    return _client


def ask_groq(
    prompt: str,
    model: str = "smart",
    temperature: float = 0.7,
    system_prompt: Optional[str] = None,
) -> AgentResponse:
    """
    Simple interface to Groq via LiteLLM.

    Args:
        prompt: User prompt
        model: "fast", "balanced", "smart", or "reasoning"
        temperature: Sampling temperature (0-2)
        system_prompt: Optional system prompt

    Returns:
        AgentResponse with content and metadata
    """
    actual_model = MODELS.get(model, MODELS["smart"])
    client = get_client()
    return client.complete(
        prompt=prompt,
        model=actual_model,
        system_prompt=system_prompt,
        temperature=temperature,
    )


def analyze_code(
    code: str,
    task: str = "review",
    language: str = "python",
) -> AgentResponse:
    """
    Analyze code for review, refactor, or explain.

    Args:
        code: Code to analyze
        task: "review", "refactor", "explain", "test"
        language: Programming language

    Returns:
        AgentResponse with analysis
    """
    prompts = {
        "review": f"Review this {language} code for bugs, security issues, and improvements:\n\n```{language}\n{code}\n```",
        "refactor": f"Refactor this {language} code for better readability and performance:\n\n```{language}\n{code}\n```",
        "explain": f"Explain what this {language} code does:\n\n```{language}\n{code}\n```",
        "test": f"Write unit tests for this {language} code:\n\n```{language}\n{code}\n```",
    }

    prompt = prompts.get(task, prompts["review"])

    system_prompt = f"You are a {language} expert. Provide clear, actionable feedback."

    return ask_groq(prompt, model="smart", system_prompt=system_prompt)


def research_task(
    topic: str,
    format: str = "markdown",
    max_items: int = 10,
) -> AgentResponse:
    """
    Research a topic and return structured findings.

    Args:
        topic: Research topic
        format: "markdown", "json", or "table"
        max_items: Maximum items to return

    Returns:
        AgentResponse with research findings
    """
    prompt = f"""Research: {topic}

Provide {max_items} key findings in {format} format.
Include:
- Key facts
- Numbers and statistics where available
- Sources
- Recommendations"""

    return ask_groq(prompt, model="balanced")


def batch_parallel(
    tasks: List[Dict[str, str]],
    model: str = "fast",
) -> List[AgentResponse]:
    """
    Run multiple tasks in parallel (simulated).

    Args:
        tasks: List of {"prompt": "...", "system": "..."} dicts
        model: Model to use

    Returns:
        List of AgentResponses
    """
    results = []
    for task in tasks:
        result = ask_groq(
            prompt=task.get("prompt", ""),
            model=model,
            system_prompt=task.get("system"),
        )
        results.append(result)
    return results


def health_check() -> Dict[str, Any]:
    """
    Check LiteLLM and Groq availability.

    Returns:
        Health status dictionary
    """
    import requests

    status = {
        "litellm": {"status": "unknown", "url": LITELLM_URL},
        "groq": {"status": "unknown", "api_key_set": bool(GROQ_API_KEY)},
    }

    # Check LiteLLM
    try:
        headers = {"Authorization": f"Bearer {LITELLM_MASTER_KEY}"}
        response = requests.get(f"{LITELLM_URL}/health", headers=headers, timeout=5)
        status["litellm"]["status"] = (
            "healthy" if response.status_code == 200 else "error"
        )
    except Exception as e:
        status["litellm"]["status"] = "unreachable"
        status["litellm"]["error"] = str(e)

    # Check Groq directly
    try:
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            timeout=5,
        )
        status["groq"]["status"] = "healthy" if response.status_code == 200 else "error"
    except Exception as e:
        status["groq"]["status"] = "unreachable"
        status["groq"]["error"] = str(e)

    return status


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Tools CLI")
    parser.add_argument("command", choices=["ask", "analyze", "research", "health"])
    parser.add_argument("--prompt", "-p", help="Prompt or topic")
    parser.add_argument("--model", "-m", default="smart", choices=list(MODELS.keys()))

    args = parser.parse_args()

    if args.command == "health":
        result = health_check()
        print(json.dumps(result, indent=2))
    elif args.command == "ask":
        if not args.prompt:
            print("Error: --prompt required")
            sys.exit(1)
        result = ask_groq(args.prompt, model=args.model)
        print(result.content if result.success else f"Error: {result.error}")
    elif args.command == "research":
        if not args.prompt:
            print("Error: --prompt required")
            sys.exit(1)
        result = research_task(args.prompt)
        print(result.content if result.success else f"Error: {result.error}")
