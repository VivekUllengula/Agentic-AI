import os

import gradio as gr
from ollama import chat

# Basic configurable defaults via env (optional)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
SYSTEM_PROMPT = os.getenv(
    "OLLAMA_SYSTEM_PROMPT",
    "You are a concise, helpful assistant. Keep answers brief and clear.",
)

def build_messages(message, history):
    """Build Ollama messages from a simple list of {role, content} dicts.

    - history: list of dicts like {"role": "user"|"assistant", "content": str}
      (Tuples like (user, assistant) are also handled for convenience.)
    - message: str or dict with {"content": str}
    """
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

    for item in history or []:
        if isinstance(item, dict) and "role" in item and "content" in item:
            role = "assistant" if item["role"] in ("assistant", "model") else "user"
            messages.append({"role": role, "content": str(item["content"])})
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            user_msg, bot_msg = item[0], item[1]
            if user_msg:
                messages.append({"role": "user", "content": str(user_msg)})
            if bot_msg:
                messages.append({"role": "assistant", "content": str(bot_msg)})

    current_text = message.get("content") if isinstance(message, dict) else str(message)
    messages.append({"role": "user", "content": current_text})
    return messages


def stream_ollama_reply(message, history):
    """Stream a reply from Ollama using a simple dict-based history."""
    messages = build_messages(message, history)

    try:
        stream = chat(model=OLLAMA_MODEL, messages=messages, stream=True)
    except Exception as e:
        yield f"[Error connecting to Ollama/model '{OLLAMA_MODEL}']: {e}"
        return

    partial = ""
    try:
        for chunk in stream:
            content = None
            if hasattr(chunk, "message") and getattr(chunk.message, "content", None):
                content = chunk.message.content
            elif isinstance(chunk, dict):
                content = chunk.get("message", {}).get("content") or chunk.get("content")
            if content:
                partial += content
                yield partial
    except Exception as e:
        yield f"[Streaming error]: {e}"


demo = gr.ChatInterface(
    fn=stream_ollama_reply,
    title=f"Ollama Chat • {OLLAMA_MODEL}",
    description=(
        "Chat with a local Ollama model. Set `OLLAMA_MODEL` and `OLLAMA_SYSTEM_PROMPT` "
        "env vars to customize."
    ),
    type="messages",
)


if __name__ == "__main__":
    # Launch on a stable default port; change via CLI if desired
    demo.launch()


