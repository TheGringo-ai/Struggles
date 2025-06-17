import os

def load_secrets():
    """Load secrets from environment variables (injected via GCP or .env)."""
    return {
        "openai_key": os.getenv("OPENAI_API_KEY", ""),
        "gemini_key": os.getenv("GEMINI_API_KEY", ""),
        "huggingface_key": os.getenv("HUGGINGFACE_API_KEY", ""),
        "custom_auth": os.getenv("CUSTOM_AUTH_HEADER", ""),
        "custom_url": os.getenv("CUSTOM_API_URL", "")
    }

def explain_secrets():
    """Show current loaded state and copy-paste friendly keys."""
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "[Not Set]"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "[Not Set]"),
        "HUGGINGFACE_API_KEY": os.getenv("HUGGINGFACE_API_KEY", "[Not Set]"),
        "CUSTOM_AUTH_HEADER": os.getenv("CUSTOM_AUTH_HEADER", "[Not Set]"),
        "CUSTOM_API_URL": os.getenv("CUSTOM_API_URL", "[Not Set]")
    }
