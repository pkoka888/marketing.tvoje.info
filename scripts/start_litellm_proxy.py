import sys
import os

# Force path
site_packages = r"C:\Users\HP\AppData\Local\Programs\Python\Python313\Lib\site-packages"
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

print(f"Python executable: {sys.executable}")
print(f"sys.path: {sys.path[:3]}...") # Print first 3 to avoid spam

try:
    import litellm
    print(f"LiteLLM found at: {litellm.__file__}")
except ImportError as e:
    print(f"Failed to import litellm: {e}")
    sys.exit(1)

# Try to import run_server or main entry point
try:
    from litellm.proxy.proxy_server import run_server
    print("Successfully imported run_server from litellm.proxy.proxy_server")
    ENTRY_POINT = run_server
except ImportError:
    print("Could not import run_server. Trying other paths...")
    try:
        from litellm.proxy.proxy_cli import run_server
        print("Successfully imported run_server from litellm.proxy.proxy_cli")
        ENTRY_POINT = run_server
    except ImportError as e:
         print(f"Failed to import run_server: {e}")
         sys.exit(1)

if __name__ == "__main__":
    print("Starting LiteLLM Proxy...")
    config_path = os.path.join(os.getcwd(), "litellm", "proxy_config.yaml")

    # Simulate CLI arguments
    sys.argv = ["litellm", "--config", config_path, "--port", "4000", "--debug"]

    try:
        # Some versions of litellm use click which reads sys.argv automatically
        print(f"Invoking entry point: {ENTRY_POINT}")
        ENTRY_POINT()
    except Exception as e:
        print(f"Runtime error: {e}")
        import traceback
        traceback.print_exc()
