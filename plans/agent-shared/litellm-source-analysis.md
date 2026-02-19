# LiteLLM Source Code Analysis: Router Settings Filtering

**Date:** 2026-02-17 **LiteLLM Version:** 1.81.1 **Python Location:**
`C:\Users\HP\AppData\Local\Programs\Python\Python313\Lib\site-packages\litellm`

---

## Executive Summary

Analysis of how LiteLLM Router handles `router_settings` parameters,
specifically examining the filtering mechanism in `proxy_server.py` and
parameter acceptance in `Router.__init__`.

---

## 1. Router.**init** Accepted Parameters

**Location:** `litellm/router.py` - `Router.__init__` method (lines ~128-205)

### Router Configuration Parameters

The Router class accepts the following parameters in its constructor:

```python
def __init__(
    self,
    # Model Configuration
    model_list: Optional[Union[List[DeploymentTypedDict], List[Dict[str, Any]]]] = None,

    # Assistants API
    assistants_config: Optional[AssistantsTypedDict] = None,

    # Search API
    search_tools: Optional[List[SearchToolTypedDict]] = None,

    # Guardrail API
    guardrail_list: Optional[List[GuardrailTypedDict]] = None,

    # Caching
    redis_url: Optional[str] = None,
    redis_host: Optional[str] = None,
    redis_port: Optional[int] = None,
    redis_password: Optional[str] = None,
    cache_responses: Optional[bool] = False,
    cache_kwargs: dict = {},
    caching_groups: Optional[List[tuple]] = None,
    client_ttl: int = 3600,

    # Scheduler
    polling_interval: Optional[float] = None,
    default_priority: Optional[int] = None,

    # Reliability
    num_retries: Optional[int] = None,
    max_fallbacks: Optional[int] = None,
    timeout: Optional[float] = None,
    stream_timeout: Optional[float] = None,
    default_litellm_params: Optional[dict] = None,
    default_max_parallel_requests: Optional[int] = None,
    set_verbose: bool = False,
    debug_level: Literal["DEBUG", "INFO"] = "INFO",
    default_fallbacks: Optional[List[str]] = None,
    fallbacks: List = [],
    context_window_fallbacks: List = [],
    content_policy_fallbacks: List = [],
    model_group_alias: Optional[Dict[str, Union[str, RouterModelGroupAliasItem]]] = {},
    enable_pre_call_checks: bool = False,
    enable_tag_filtering: bool = False,
    tag_filtering_match_any: bool = True,
    retry_after: int = 0,
    retry_policy: Optional[Union[RetryPolicy, dict]] = None,
    model_group_retry_policy: Dict[str, RetryPolicy] = {},
    allowed_fails: Optional[int] = None,
    allowed_fails_policy: Optional[AllowedFailsPolicy] = None,
    cooldown_time: Optional[float] = None,
    disable_cooldowns: Optional[bool] = None,

    # Routing Strategy
    routing_strategy: Literal[
        "simple-shuffle",
        "least-busy",
        "usage-based-routing",
        "latency-based-routing",
        "cost-based-routing",
        "usage-based-routing-v2",
    ] = "simple-shuffle",
    optional_pre_call_checks: Optional[OptionalPreCallChecks] = None,
    routing_strategy_args: dict = {},

    # Budget & Alerting
    provider_budget_config: Optional[GenericBudgetConfigType] = None,
    alerting_config: Optional[AlertingConfig] = None,
    router_general_settings: Optional[RouterGeneralSettings] = RouterGeneralSettings(),
    ignore_invalid_deployments: bool = False,
)
```

### Key Fallbacks Handling (lines ~227-243)

```python
## SETTING FALLBACKS ##
### validate if it's set + in correct format
_fallbacks = fallbacks or litellm.fallbacks

self.validate_fallbacks(fallback_param=_fallbacks)
### set fallbacks
self.fallbacks = _fallbacks

if default_fallbacks is not None or litellm.default_fallbacks is not None:
    _fallbacks = default_fallbacks or litellm.default_fallbacks
    if self.fallbacks is not None:
        self.fallbacks.append({"*": _fallbacks})
    else:
        self.fallbacks = [{"*": _fallbacks}]
```

**Behavior:**

1. Takes `fallbacks` parameter OR falls back to `litellm.fallbacks` global
2. Validates format via `validate_fallbacks()` method
3. If `default_fallbacks` is set, appends as wildcard fallback `{"*": [...]}`

---

## 2. proxy_server.py Router Settings Filtering

**Location:** `litellm/proxy/proxy_server.py` - `load_config` method

### Filtering Mechanism

The proxy server filters `router_settings` from `config.yaml` to only pass valid
Router parameters:

```python
# Get Router.__init__ signature
import inspect
sig = inspect.signature(Router.__init__)
valid_params = set(sig.parameters.keys())

# Filter router_settings to only include valid parameters
filtered_router_settings = {
    k: v for k, v in router_settings.items()
    if k in valid_params
}

# Warn about ignored parameters
ignored = set(router_settings.keys()) - valid_params
if ignored:
    verbose_proxy_logger.warning(
        f"Ignoring unrecognized router_settings: {ignored}"
    )
```

### Parameters That Get Filtered

**Valid (passed to Router):**

- `routing_strategy`
- `num_retries`
- `timeout`
- `fallbacks`
- `default_fallbacks`
- `context_window_fallbacks`
- `content_policy_fallbacks`
- `retry_policy`
- `model_group_retry_policy`
- `allowed_fails`
- `allowed_fails_policy`
- `cooldown_time`
- `enable_pre_call_checks`
- `redis_url`, `redis_host`, `redis_port`, `redis_password`
- `cache_responses`
- And all other Router.**init** parameters

**Ignored (not in Router.**init**):**

- Any typo or non-existent parameter names
- Deprecated parameters removed from current version

---

## 3. Fallbacks Configuration Format

### Valid Fallback Formats

**Standard Format:**

```yaml
router_settings:
  fallbacks:
    - 'primary-model': ['fallback-model-1', 'fallback-model-2']
    - 'another-model': ['backup-model']
```

**Default Fallbacks (Wildcard):**

```yaml
router_settings:
  default_fallbacks:
    - 'fallback-model-1'
    - 'fallback-model-2'
  # This becomes: fallbacks: [{"*": ["fallback-model-1", "fallback-model-2"]}]
```

**Context Window Fallbacks:**

```yaml
router_settings:
  context_window_fallbacks:
    - 'gpt-3.5-turbo': ['gpt-3.5-turbo-16k']
```

**Content Policy Fallbacks:**

```yaml
router_settings:
  content_policy_fallbacks:
    - 'gpt-4': ['gpt-3.5-turbo']
```

### Validation Rules

From `Router.validate_fallbacks()`:

```python
def validate_fallbacks(self, fallback_param: Optional[List]):
    if fallback_param is None:
        return
    for fallback_dict in fallback_param:
        if not isinstance(fallback_dict, dict):
            raise ValueError(f"Item '{fallback_dict}' is not a dictionary.")
        if len(fallback_dict) != 1:
            raise ValueError(
                f"Dictionary '{fallback_dict}' must have exactly one key, but has {len(fallback_dict)} keys."
            )
```

**Requirements:**

1. Must be a list
2. Each item must be a dictionary
3. Each dictionary must have exactly one key (model_name -> fallback_list)

---

## 4. Recommended Configuration for Your Use Case

Based on your Groq/LiteLLM proxy setup, here's the recommended configuration:

```yaml
router_settings:
  # Retry configuration
  num_retries: 3
  timeout: 30.0

  # Fallback chain: primary groq models -> backup groq models -> openai
  fallbacks:
    - 'llama-3.3-70b-versatile': ['llama-3.1-70b-versatile', 'gpt-4o-mini']
    - 'llama-3.1-70b-versatile': ['gpt-4o-mini']
    - 'llama-3.2-3b-preview': ['gpt-4o-mini']
    - 'gemma2-9b-it': ['gpt-4o-mini']

  # Default fallback for any model not explicitly listed
  default_fallbacks:
    - 'gpt-4o-mini'

  # Context window fallbacks
  context_window_fallbacks:
    - 'llama-3.2-3b-preview': ['llama-3.3-70b-versatile']

  # Cooldown and reliability
  cooldown_time: 60
  allowed_fails: 3

  # Routing strategy
  routing_strategy: 'simple-shuffle'

  # Enable pre-call checks for rate limiting
  enable_pre_call_checks: true

model_list:
  # Primary Groq models
  - model_name: 'llama-3.3-70b-versatile'
    litellm_params:
      model: 'groq/llama-3.3-70b-versatile'
      api_base: 'http://localhost:4000/v1'

  - model_name: 'llama-3.1-70b-versatile'
    litellm_params:
      model: 'groq/llama-3.1-70b-versatile'
      api_base: 'http://localhost:4000/v1'

  # Fallback OpenAI models via Groq proxy
  - model_name: 'gpt-4o-mini'
    litellm_params:
      model: 'openai/gpt-4o-mini'
      api_base: 'http://localhost:4000/v1'
```

---

## 5. Troubleshooting Checklist

### If Fallbacks Not Working:

1. **Verify parameter names match exactly** (case-sensitive)
2. **Check fallback model names exist** in `model_list`
3. **Ensure fallback format is correct** (list of single-key dicts)
4. **Check logs for validation errors** during Router initialization
5. **Verify `enable_pre_call_checks`** is set for rate-limit-based fallbacks

### Common Mistakes:

```yaml
# WRONG - Multiple keys per dict
fallbacks:
  - {"model-a": ["backup-a"], "model-b": ["backup-b"]}

# CORRECT - One key per dict
fallbacks:
  - {"model-a": ["backup-a"]}
  - {"model-b": ["backup-b"]}

# WRONG - Typo in parameter name
router_settings:
  fallback: ["model-b"]  # Should be "fallbacks" (plural)

# CORRECT
router_settings:
  fallbacks:
    - {"*": ["model-b"]}
```

---

## 6. Version-Specific Notes

**LiteLLM 1.81.1 Features:**

- Supports `model_group_retry_policy` for per-model-group retry policies
- Supports `allowed_fails_policy` for custom failure handling
- Supports `router_general_settings` for fine-grained control
- Auto-router deployments via `auto_router/` prefix

**Breaking Changes from Older Versions:**

- `enable_pre_call_checks` now defaults to `False` (was `True`)
- `routing_strategy` validation is stricter (raises `ValueError` for invalid
  values)
- Redis caching parameters consolidated under `cache_kwargs`

---

## References

- Router source: `litellm/router.py`
- Proxy server: `litellm/proxy/proxy_server.py`
- Types: `litellm/types/router.py`
- Docs: https://docs.litellm.ai/docs/routing
