import requests
import json
import base64


def call_agent(prompt, model, provider, api_key, secrets, temperature=0.7, top_p=1.0,
               tools=None, stream=False, image=None, memory_enabled=False, chaining_enabled=False):
    # Tool chaining or memory logic could be handled here or routed to a dedicated module
    if chaining_enabled:
        from agents.chained_agent import run_chained_agents
        return run_chained_agents(prompt, model, provider, api_key, secrets, temperature, top_p, tools, image)

    if provider == "OpenAI":
        return call_openai(prompt, model, api_key, temperature, top_p, tools, stream, image)
    elif provider == "Gemini":
        return call_gemini(prompt, model, api_key, temperature, top_p, image)
    elif provider == "HuggingFace":
        return call_huggingface(prompt, model, api_key)
    elif provider == "Custom":
        return call_custom(prompt, model, secrets)
    else:
        return f"⚠️ Unknown provider: {provider}"


def call_openai(prompt, model, api_key, temperature, top_p, tools, stream, image=None):
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
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI API Error: {str(e)}"


def call_gemini(prompt, model, api_key, temperature, top_p, image=None):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}

        parts = [{"text": prompt}]
        if image:
            image_data = image.read()
            b64_image = base64.b64encode(image_data).decode("utf-8")
            parts.append({
                "inlineData": {
                    "mimeType": image.type,
                    "data": b64_image
                }
            })

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": temperature,
                "topP": top_p
            }
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Gemini API Error: {str(e)}"


def call_huggingface(prompt, model, api_key):
    try:
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"❌ HuggingFace API Error: {str(e)}"


def call_custom(prompt, model, secrets):
    try:
        url = secrets.get("custom_url", "")
        auth_header = secrets.get("custom_auth", "")
        if not url:
            return "❌ Custom API URL not set."

        headers = {"Content-Type": "application/json"}
        if auth_header:
            headers["Authorization"] = auth_header

        payload = {
            "prompt": prompt,
            "model": model
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        data = response.json()
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"❌ Custom API Error: {str(e)}"