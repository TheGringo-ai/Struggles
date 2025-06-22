import streamlit as st
from agent_caller import call_agent
from firebase_admin import firestore
from datetime import datetime

AGENT_PRESETS = {
    "Raw": "",
    "Trainer": "You are a multilingual training assistant. Convert this into an instructional format with steps.",
    "MaintenanceBot": "You are a maintenance diagnostics AI. Provide a root-cause analysis and a repair plan.",
    "Translator": "Translate the following input to Spanish, but keep any technical terms in English."
}

st.sidebar.markdown("---")
agent_role = st.sidebar.selectbox("Select Agent Role", list(AGENT_PRESETS.keys()))

user_input = st.text_area("Enter your prompt here:")

if st.button("Submit"):
    system_prompt = AGENT_PRESETS.get(agent_role, "")
    full_prompt = f"{system_prompt}\n\n{user_input}" if system_prompt else user_input
    response = call_agent(provider="OpenAI", prompt=full_prompt, model="gpt-4", api_key="your_api_key", temperature=0.7, top_p=1, tools=None, stream=False)
    st.write(response)
    try:
        db = firestore.client()
        user_email = st.session_state.get("user", {}).get("email", "anonymous")
        db.collection("ai_logs").add({
            "user": user_email,
            "prompt": user_input,
            "role": agent_role,
            "model": "gpt-4",
            "response_length": len(response) if response else 0,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        st.warning(f"Logging failed: {e}")