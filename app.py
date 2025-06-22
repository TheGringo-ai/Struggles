import os
import sys
import streamlit as st
from dotenv import load_dotenv
from utils.agent_runner import safely_call_agent

# ──────────────── Setup ────────────────
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)
os.environ["PYTHONPATH"] = APP_ROOT

load_dotenv()

from model_selector import (
    MODEL_PRESETS,
    get_model_description,
    get_model,
    get_provider,
    get_api_key,
)
from agent_caller import call_agent

# ──────────────── Secrets ────────────────
try:
    from utils.secrets import load_secrets, explain_secrets
    secrets = load_secrets() or {}
except ModuleNotFoundError as e:
    st.warning(f"⚠️ Secrets module not found: {e}")
    secrets = {}
    def explain_secrets(_=None):
        return {"Warning": "[utils/secrets.py not found or import failed]"}

# ──────────────── UI CONFIG ────────────────
st.set_page_config(page_title="Struggles AI - Agent Core", layout="wide")
st.title("🤖 Struggles AI – Agent Core")
st.caption("Multi-agent AI control panel (OpenAI / Gemini / Hugging Face / Custom)")

# ──────────────── Sidebar: Model Selection ────────────────
st.sidebar.markdown("### ⚙️ Model Selector")
provider = st.sidebar.selectbox("AI Provider", ["OpenAI", "Gemini", "HuggingFace", "Custom"], key="provider")
models = list(MODEL_PRESETS.get(provider, {}).keys())

use_custom_model = st.sidebar.checkbox("✏️ Enter custom model ID", value=False)

if use_custom_model:
    st.session_state["model"] = st.sidebar.text_input("Custom Model ID", key="custom_model")
    st.sidebar.caption("🛠️ Using custom model.")
else:
    if "model" not in st.session_state and models:
        st.session_state["model"] = models[0]
    selected_model = st.sidebar.selectbox("Model ID", models, key="model")
    desc = get_model_description(provider, selected_model)
    st.sidebar.caption(f"ℹ️ {desc}")

# ──────────────── Sidebar: API Keys ────────────────
if provider == "OpenAI":
    st.session_state["openai_key"] = st.sidebar.text_input("OpenAI API Key", type="password")
elif provider == "Gemini":
    st.session_state["gemini_key"] = st.sidebar.text_input("Gemini API Key", type="password")
elif provider == "HuggingFace":
    st.session_state["huggingface_key"] = st.sidebar.text_input("Hugging Face API Key", type="password")
elif provider == "Custom":
    st.session_state["custom_url"] = st.sidebar.text_input("Custom Endpoint URL")
    st.session_state["custom_auth"] = st.sidebar.text_input("Custom Auth Header", type="password")

# ──────────────── Sidebar: Model Settings ────────────────
st.sidebar.markdown("### 🎛️ Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 1.0, 0.05)
stream = st.sidebar.toggle("📡 Stream Response", value=False)

# ──────────────── Sidebar: Tools + Options ────────────────
st.sidebar.markdown("### 🛠️ Tool Usage")
use_retrieval = st.sidebar.checkbox("Enable Retrieval")
use_code = st.sidebar.checkbox("Enable Code Interpreter")
enable_memory = st.sidebar.checkbox("🧠 Enable Memory Between Calls")
enable_chaining = st.sidebar.checkbox("⛓️ Chain Agents")

tools = []
if use_retrieval: tools.append("retrieval")
if use_code: tools.append("code_interpreter")

# ──────────────── Main Input + Vision ────────────────
user_input = st.text_area("💬 Enter your command or request:", height=200)
uploaded_image = None
if provider in ["OpenAI", "Gemini"] and "vision" in st.session_state["model"]:
    uploaded_image = st.file_uploader("📷 Upload image for vision model", type=["jpg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Input for vision model")

# ──────────────── Call Agent ────────────────
if st.button("Run Agent"):
    with st.spinner("Calling agent..."):
        response = safely_call_agent(
            provider=provider,
            model=st.session_state["model"],
            prompt=user_input,
            session_state=st.session_state,
            temperature=temperature,
            top_p=top_p,
            tools=tools,
            stream=stream,
            image=uploaded_image,
            memory_enabled=enable_memory,
            chaining_enabled=enable_chaining,
            secrets=secrets
        )
        if response:
            st.markdown("### 🧠 Agent Response")
            st.code(response, language="markdown")

# ──────────────── Debug + Secrets Info ────────────────
with st.expander("📜 Debug Logs"):
    st.json({
        "input": user_input,
        "model": st.session_state.get("model"),
        "provider": provider,
        "temperature": temperature,
        "top_p": top_p,
        "tools": tools,
        "stream": stream,
        "memory": enable_memory,
        "chaining": enable_chaining
    })

with st.expander("🔐 Secret Setup Guide"):
    st.markdown("Set these as environment variables locally or in Google Cloud Secret Manager:")
    st.code("""
OPENAI_API_KEY=sk-xxxx
GEMINI_API_KEY=your-gemini-key
HUGGINGFACE_API_KEY=hf_xxxx
CUSTOM_AUTH_HEADER=Bearer your-token
CUSTOM_API_URL=https://your.custom.api
""", language="bash")

    st.markdown("### 🧪 Detected Secrets:")
    try:
        for k, v in explain_secrets(secrets or {}).items():
            status = "✅ Loaded" if "[Not Set]" not in v else "❌ Missing"
            st.text(f"{k}: {status}")
    except Exception as e:
        st.error(f"Unable to explain secrets: {e}")