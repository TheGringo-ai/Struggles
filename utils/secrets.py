import os
from dotenv import load_dotenv

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None

load_dotenv()

def load_secrets(keys=None):
    """
    Load secrets from Google Secret Manager or .env fallback.
    If `keys` is provided, only those keys are loaded.
    """
    secrets = {}
    project_id = os.getenv("GCP_PROJECT_ID")

    if secretmanager and project_id:
        client = secretmanager.SecretManagerServiceClient()
        for key in (keys or os.environ.keys()):
            try:
                name = f"projects/{project_id}/secrets/{key}/versions/latest"
                response = client.access_secret_version(name=name)
                secrets[key] = response.payload.data.decode("UTF-8")
            except Exception:
                secrets[key] = os.getenv(key)
    else:
        for key in (keys or os.environ.keys()):
            secrets[key] = os.getenv(key)

    return secrets


def explain_secrets(secrets):
    print("🔐 Loaded Secrets:")
    for k in secrets:
        print(f" - {k}: {'✅' if secrets[k] else '⚠️ MISSING'}")