import os

TEMPLATE = {
    "OPENAI_API_KEY": "sk-...",
    "GOOGLE_API_KEY": "your-google-api-key",
    "HUGGINGFACE_TOKEN": "your-huggingface-token"
}

env_path = ".env"
if os.path.exists(env_path):
    print("⚠️ .env already exists. Skipping.")
else:
    with open(env_path, "w") as f:
        for key, value in TEMPLATE.items():
            f.write(f"{key}={value}\n")
    print("✅ .env file created.")