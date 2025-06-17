import streamlit as st
from model_selector import MODEL_PRESETS, get_model_description, get_model, get_provider, get_api_key
from agent_caller import call_agent
from secrets import load_secrets, explain_secrets

# ───────────────────────────────────────────────
# PAGE CONFIG
# ───────────────────────────────────────────────
st.set_page_config(page_title="Struggles AI - Agent Core", layout="wide")
st.title("🤖 Struggles AI – Agent Core")
st.caption("Multi-agent AI control panel (OpenAI / Gemini / Hugging Face / Custom)")

# ───────────────────────────────────────────────
# LOAD SECRETS
# ───────────────────────────────────────────────
secrets = load_secrets()

# ───────────────────────────────────────────────
# SIDEBAR: Provider + Model Selection
# ───────────────────────────────────────────────
st.sidebar.markdown("### ⚙️ Model Selector")

provider = st.sidebar.selectbox("AI Provider", ["OpenAI", "Gemini", "HuggingFace", "Custom"], key="provider")
models = list(MODEL_PRESETS.get(provider, {}).keys())

use_custom_model = st.sidebar.checkbox("✏️ Enter custom model ID", value=False)
if use_custom_model:
    st.session_state["model"] = st.sidebar.text_input("Custom Model ID", key="model")
    st.sidebar.caption("🛠️ Using custom model.")
else:
    st.session_state["model"] = st.sidebar.selectbox("Model ID", models, key="model")
    desc = get_model_description(provider, st.session_state["model"])
    st.sidebar.caption(f"ℹ️ {desc}")

# ───────────────────────────────────────────────
# API Keys
# ───────────────────────────────────────────────
if provider == "OpenAI":
    st.session_state["openai_key"] = st.sidebar.text_input("OpenAI API Key", type="password")
elif provider == "Gemini":
    st.session_state["gemini_key"] = st.sidebar.text_input("Gemini API Key", type="password")
elif provider == "HuggingFace":
    st.session_state["huggingface_key"] = st.sidebar.text_input("Hugging Face API Key", type="password")
elif provider == "Custom":
    st.session_state["custom_url"] = st.sidebar.text_input("Custom Endpoint URL")
    st.session_state["custom_auth"] = st.sidebar.text_input("Custom Auth Header", type="password")

# ───────────────────────────────────────────────
# ADVANCED SETTINGS
# ───────────────────────────────────────────────
st.sidebar.markdown("### 🎛️ Model Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 1.0, 0.05)
stream = st.sidebar.toggle("📡 Stream Response", value=False)

# ───────────────────────────────────────────────
# TOOL + CHAIN OPTIONS
# ───────────────────────────────────────────────
st.sidebar.markdown("### 🛠️ Tool Usage")
use_retrieval = st.sidebar.checkbox("Enable Retrieval")
use_code = st.sidebar.checkbox("Enable Code Interpreter")
enable_memory = st.sidebar.checkbox("🧠 Enable Memory Between Calls")
enable_chaining = st.sidebar.checkbox("⛓️ Chain Agents")

tools = []
if use_retrieval:
    tools.append("retrieval")
if use_code:
    tools.append("code_interpreter")

# ───────────────────────────────────────────────
# PROMPT + VISION SUPPORT
# ───────────────────────────────────────────────
user_input = st.text_area("💬 Enter your command or request:", height=200)
uploaded_image = None
if provider in ["OpenAI", "Gemini"] and "vision" in st.session_state["model"]:
    uploaded_image = st.file_uploader("📷 Upload image for vision model", type=["jpg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Input for vision model")

# ───────────────────────────────────────────────
# RUN AGENT
# ───────────────────────────────────────────────
if st.button("Run Agent"):
    with st.spinner("Calling agent..."):
        response = call_agent(
            prompt=user_input,
            model=st.session_state["model"],
            provider=provider,
            api_key=get_api_key(provider, st.session_state),
            secrets=secrets,
            temperature=temperature,
            top_p=top_p,
            tools=tools,
            stream=stream,
            image=uploaded_image,
            memory_enabled=enable_memory,
            chaining_enabled=enable_chaining
        )
        st.markdown("### 🧠 Agent Response")
        st.code(response, language="markdown")

# ───────────────────────────────────────────────
# DEBUG / SECRETS
# ───────────────────────────────────────────────
with st.expander("📜 Debug Logs"):
    st.json({
        "input": user_input,
        "model": st.session_state["model"],
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
    for k, v in explain_secrets().items():
        status = "✅ Loaded" if "[Not Set]" not in v else "❌ Missing"
        st.text(f"{k}: {status}")