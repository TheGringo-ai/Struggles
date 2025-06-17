# chained_agent.py

from agent_caller import call_agent
from tools.retrieval import run_retrieval
from tools.code_interpreter import run_code_tool
from config import CHAINS, TOOL_SCORES


def chained_agent(prompt, model, provider, api_key, mode="default", secrets=None, memory=None,
                  temperature=0.7, top_p=1.0, tools=None, stream=False, image=None):
    """
    Orchestrates a multi-step toolchain based on mode or config.
    Supports chaining, scoring, and shared memory state.
    """
    memory = memory or {}  # Persistent memory store between steps

    def step_result(tool, input_text):
        if tool == "retrieval":
            result = run_retrieval(input_text)
            memory["retrieval"] = result
            return result

        elif tool == "code":
            result = run_code_tool(input_text)
            memory["code"] = result
            return result

        elif tool == "model":
            # Adjust prompt based on previous context
            context = ""
            if "retrieval" in memory:
                context += f"\n\nRelevant Docs:\n{memory['retrieval']}"
            if "code" in memory:
                context += f"\n\nCode Analysis:\n{memory['code']}"
            full_prompt = f"{input_text}{context}"

            result = call_agent(
                prompt=full_prompt,
                model=model,
                provider=provider,
                api_key=api_key,
                secrets=secrets,
                temperature=temperature,
                top_p=top_p,
                tools=tools,
                stream=stream,
                image=image,
                memory_enabled=True,
                chaining_enabled=False  # prevent recursion
            )
            memory["model"] = result
            return result

        else:
            raise ValueError(f"Unknown tool: {tool}")

    # Use pre-defined chain logic
    if mode in CHAINS:
        chain = CHAINS[mode]
        current_input = prompt

        for step_tool in chain:
            current_input = step_result(step_tool, current_input)

        return memory.get("model", current_input)

    else:
        # Default to single model call if no chain matched
        return call_agent(
            prompt=prompt,
            model=model,
            provider=provider,
            api_key=api_key,
            secrets=secrets,
            temperature=temperature,
            top_p=top_p,
            tools=tools,
            stream=stream,
            image=image
        )