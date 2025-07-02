import streamlit as st


# Preset models for each provider
MODEL_PRESETS = {
    "OpenAI": {
        "gpt-4-0125-preview": "Most powerful GPT-4 model for reasoning and code.",
        "gpt-3.5-turbo": "Fast, cheap, and lightweight for most tasks."
    },
    "Gemini": {
        "gemini-pro": "Google’s Gemini Pro (v1) - basic flagship model.",
        "gemini-1.5-pro": "Gemini 1.5 Pro (Latest) - strong reasoning and multi-modal support.",
        "gemini-1.5-flash": "Gemini 1.5 Flash - optimized for speed and low latency."
    },
    "HuggingFace": {
        "mistralai/Mistral-7B-Instruct-v0.2": "7B open-weight model for coding and QA.",
        "meta-llama/Llama-2-13b-chat-hf": "LLaMA 2 model fine-tuned for chat."
    },
    "Custom": {
        "your-model-id": "Your custom endpoint model."
    }
}


def get_provider():
    return st.session_state.get("provider", "OpenAI")


def get_model():
    return st.session_state.get("model", "gpt-4-0125-preview")


def get_api_key(provider, state=None):
    state = state or st.session_state
    key_name = f"{provider.lower()}_key"
    return state.get(key_name, "")


def get_model_description(provider, model_id):
    """Return model description if known."""
    return MODEL_PRESETS.get(provider, {}).get(model_id, "🔍 Custom or unknown model.")


def get_fallback_model(provider, failed_model):
    models = list(MODEL_PRESETS.get(provider, {}).keys())
    if failed_model in models:
        models.remove(failed_model)
    return models[0] if models else None


def render_model_selector(provider):
    model_descriptions = MODEL_PRESETS.get(provider, {})
    model_options = list(model_descriptions.keys())
    labeled_options = [f"{model} – {desc}" for model, desc in model_descriptions.items()]
    selected_label = st.selectbox("Choose model:", labeled_options)
    selected_model = selected_label.split(" – ")[0]
    st.session_state["model"] = selected_model
    return selected_model