# utils/agent_runner.py

import streamlit as st
from agent_caller import call_agent
from model_selector import get_api_key

def safely_call_agent(
    provider,
    model,
    prompt,
    session_state,
    temperature=0.7,
    top_p=1.0,
    tools=None,
    stream=False,
    image=None,
    memory_enabled=False,
    chaining_enabled=False,
    secrets=None
):
    try:
        return call_agent(
            provider=provider,
            prompt=prompt,
            model=model,
            api_key=get_api_key(provider, session_state),
            temperature=temperature,
            top_p=top_p,
            tools=tools or [],
            stream=stream,
            image=image,
            memory_enabled=memory_enabled,
            chaining_enabled=chaining_enabled,
            secrets=secrets
        )
    except Exception as e:
        st.error(f"❌ Agent call failed: {e}")
        return None