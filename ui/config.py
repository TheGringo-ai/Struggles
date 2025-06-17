# config.py

# ✅ Predefined agent chains for multi-step logic
CHAINS = {
    "doc_qa_chain": ["retrieval", "model"],
    "code_first_chain": ["code", "model"],
    "deep_analysis": ["retrieval", "code", "model"],
    "custom_chain_example": ["retrieval", "model", "retrieval"]  # You can loop or repeat steps too
}

# 🧠 Tool scoring (for dynamic agent selection, ranking, or future heuristics)
TOOL_SCORES = {
    "retrieval": 0.9,
    "code": 0.8,
    "model": 1.0
}

# 🔁 Memory behavior toggle
MEMORY_ENABLED = True  # global switch to enable/disable memory across agents

# 🗃️ Memory config for Firestore (Cloud memory layer)
FIRESTORE_CONFIG = {
    "enabled": True,
    "collection": "agent_memory",
    "document_prefix": "session_",  # You can customize this per user/session
    "project_id": "chatterfix-ui"  # Replace with your actual GCP project ID
}

# 💾 Local memory fallback (optional)
LOCAL_MEMORY_PATH = "./memory_store.json"

# Future: load external chain presets or override via dynamic config
# For example, allow runtime loading from JSON, YAML, or Firestore itself