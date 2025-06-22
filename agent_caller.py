import requests
import json
import base64
import google.generativeai as genai
from transformers import pipeline

# ───────────────────────────────────────────────
# OpenAI
# ───────────────────────────────────────────────
def call_openai(prompt, model, api_key, temperature, top_p, tools, stream, image=None, **kwargs):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        if image:
            base64_image = base64.b64encode(image.read()).decode("utf-8")
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
        }

        if tools:
            payload["tools"] = [{"type": tool} for tool in tools]

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"❌ OpenAI API Error: {response.status_code} – {response.text}"

        data = response.json()
        if "choices" not in data or not data["choices"]:
            return f"❌ OpenAI API Error: No choices returned: {json.dumps(data, indent=2)}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenAI API Error: {str(e)}"


# ───────────────────────────────────────────────
# Gemini
# ───────────────────────────────────────────────
def call_gemini(prompt, model, api_key, temperature, top_p, tools, stream, image=None, **kwargs):
    try:
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": temperature,
            "top_p": top_p
        }

        model_instance = genai.GenerativeModel(model_name=model)

        if "vision" in model.lower() and image:
            result = model_instance.generate_content(
                [prompt, image],
                generation_config=generation_config,
                stream=stream
            )
        else:
            result = model_instance.generate_content(
                prompt,
                generation_config=generation_config,
                stream=stream
            )

        return result.text if hasattr(result, "text") else str(result)

    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"


# ───────────────────────────────────────────────
# Hugging Face
# ───────────────────────────────────────────────
def call_huggingface(prompt, model, api_key, temperature, top_p, tools, stream, image=None, **kwargs):
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        api_url = f"https://api-inference.huggingface.co/models/{model}"

        payload = {"inputs": prompt, "parameters": {"temperature": temperature, "top_p": top_p}}
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"❌ Hugging Face API Error: {response.status_code} – {response.text}"

        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "[No output]")
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        return str(result)

    except Exception as e:
        return f"❌ Hugging Face API Error: {str(e)}"


# ───────────────────────────────────────────────
# Router
# ───────────────────────────────────────────────
def call_agent(provider, **kwargs):
    if provider == "OpenAI":
        return call_openai(**kwargs)
    elif provider == "Gemini":
        return call_gemini(**kwargs)
    elif provider == "HuggingFace":
        return call_huggingface(**kwargs)
    else:
        return f"❌ Unsupported provider: {provider}"