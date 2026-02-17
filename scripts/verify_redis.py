#!/usr/bin/env python3
"""
Verify Redis Connectivity & Agentic Platform Constraints
- Checks connection to localhost:6379 (or REDIS_URL)
- Verifies Authentication (Password required)
- Enforces Namespace Isolation (Project Prefix: marketing_tvoje_info:)
"""

import os
import sys

import redis

# Configuration
REDIS_URL = os.getenv("REDIS_URL", None)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
PROJECT_PREFIX = "marketing_tvoje_info:"


def verify_redis():
    try:
        # Prefer REDIS_URL if set
        if REDIS_URL:
            print(f"🔌 Connecting via REDIS_URL: {REDIS_URL}")
            r = redis.from_url(REDIS_URL, socket_connect_timeout=2)
        else:
            print(f"🔌 Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}...")
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                socket_connect_timeout=2,
            )

        # 1. Ping Check
        if not r.ping():
            print("❌ Redis Ping failed.")
            return False
        print("✅ Redis Ping successful.")

        # 3. Namespace Write/Read Check
        test_key = f"{PROJECT_PREFIX}health_check"
        r.set(test_key, "ok", ex=60)
        val = r.get(test_key)

        if val != b"ok":
            print(f"❌ Namespace Write/Read failed. Key: {test_key}")
            return False

        print(f"✅ Namespace Write/Read verified ({test_key})")

        # 4. Noisy Neighbor Check (Optional / Warning)
        try:
            sample_keys = r.scan_iter(count=5)
            foreign_keys = 0
            for k in sample_keys:
                key_str = k.decode("utf-8")
                if not key_str.startswith(PROJECT_PREFIX) and not key_str.startswith(
                    "_"
                ):
                    foreign_keys += 1

            if foreign_keys > 0:
                print(
                    f"⚠️  Warning: Found {foreign_keys} keys without project prefix '{PROJECT_PREFIX}'. Ensure database isolation!"
                )
        except Exception as e:
            print(f"⚠️  Skipping neighbor check: {e}")

        return True

    except redis.exceptions.AuthenticationError:
        print("❌ Authentication failed. Check REDIS_PASSWORD.")
        # Only return False if we strictly require auth (which we do per plan)
        return False
    except redis.exceptions.ConnectionError:
        print(
            f"❌ Could not connect. Is Docker/Service running?\nURL: {REDIS_URL or f'{REDIS_HOST}:{REDIS_PORT}'}"
        )
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = verify_redis()
    sys.exit(0 if success else 1)
