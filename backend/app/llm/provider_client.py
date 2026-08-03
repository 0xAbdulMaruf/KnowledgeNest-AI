import json
import os
from typing import Any, AsyncGenerator, Sequence

import httpx

from app.llm.ollama_client import OllamaClient


Message = tuple[str, str]


class AIProviderClient:
    def __init__(self, provider: str = "local", base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        self.provider = provider
        self.base_url = (base_url or "").strip()
        self.api_key = (api_key or "").strip()
        self.model = (model or "").strip()
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=15.0))
        self._ollama = OllamaClient(base_url=self.base_url or None, model=self.model or None)

    def _resolved_base_url(self) -> str:
        if self.base_url:
            base = self.base_url.rstrip("/")
        elif self.provider == "anthropic":
            base = "https://api.anthropic.com"
        elif self.provider == "mimo":
            base = "https://api.xiaomimimo.com/v1"
        elif self.provider == "openai":
            base = "https://api.openai.com/v1"
        else:
            base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        # Anthropic's endpoint is always /v1/messages; tolerate a user-entered /v1.
        if self.provider == "anthropic" and base.endswith("/v1"):
            base = base[:-3].rstrip("/")
        return base

    def _resolved_model(self) -> str:
        if self.model:
            return self.model
        if self.provider == "anthropic":
            return "claude-3-5-sonnet-latest"
        if self.provider == "openai":
            return "gpt-4o-mini"
        if self.provider == "mimo":
            return "mimo-v2.5-pro"
        return os.getenv("OLLAMA_MODEL", "llama3")

    def _request_format(self) -> str:
        if self.provider == "anthropic":
            return "anthropic"
        if self.provider == "mimo":
            return "anthropic" if self._resolved_base_url().endswith("/anthropic") else "openai"
        if self.provider == "openai":
            return "openai"
        return "local"

    def _request_headers(self) -> dict[str, str]:
        if self.provider == "anthropic" or (self.provider == "mimo" and self._request_format() == "anthropic"):
            return {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            }
        if self.provider in {"openai", "mimo"}:
            return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        return {"Content-Type": "application/json"}

    @staticmethod
    def _openai_messages(prompt: str, system: str, history: Sequence[Message]) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        for role, content in history:
            if role in {"user", "assistant"} and content.strip():
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt})
        return messages

    @staticmethod
    def _anthropic_messages(prompt: str, history: Sequence[Message]) -> list[dict[str, Any]]:
        messages: list[dict[str, Any]] = []
        for role, content in history:
            if role in {"user", "assistant"} and content.strip():
                # Anthropic requires alternating roles; merge consecutive messages.
                if messages and messages[-1]["role"] == role:
                    messages[-1]["content"][0]["text"] += f"\n{content}"
                else:
                    messages.append({"role": role, "content": [{"type": "text", "text": content}]})
        if messages and messages[-1]["role"] == "user":
            messages[-1]["content"][0]["text"] += f"\n\nCurrent request:\n{prompt}"
        else:
            messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})
        return messages

    async def test_connection(self) -> None:
        await self.generate(prompt="Reply with OK.", system="You are a test assistant.")

    async def generate(self, prompt: str, system: str = "", history: Sequence[Message] = ()) -> str:
        if self.provider == "local":
            history_text = "\n".join(f"{role.title()}: {content}" for role, content in history)
            if history_text:
                prompt = f"Conversation history:\n{history_text}\n\nCurrent request:\n{prompt}"
            return await self._ollama.generate(prompt=prompt, system=system)

        request_format = self._request_format()
        if request_format == "openai":
            payload: dict[str, Any] = {
                "model": self._resolved_model(),
                "messages": self._openai_messages(prompt, system, history),
                "max_completion_tokens": 2048,
                "temperature": 0.2,
                "top_p": 0.95,
                "stream": False,
            }
            response = await self._client.post(f"{self._resolved_base_url()}/chat/completions", headers=self._request_headers(), json=payload)
            response.raise_for_status()
            choices = response.json().get("choices") or []
            return str((choices[0].get("message") or {}).get("content", "")) if choices else ""

        if request_format == "anthropic":
            payload = {
                "model": self._resolved_model(),
                "max_tokens": 2048,
                "temperature": 1.0,
                "top_p": 0.95,
                "stream": False,
                "messages": self._anthropic_messages(prompt, history),
            }
            if system:
                payload["system"] = system
            response = await self._client.post(f"{self._resolved_base_url()}/v1/messages", headers=self._request_headers(), json=payload)
            response.raise_for_status()
            content = response.json().get("content") or []
            return "".join(str(item.get("text", "")) for item in content if isinstance(item, dict))

        raise ValueError(f"Unsupported provider: {self.provider}")

    async def generate_stream(self, prompt: str, system: str = "", history: Sequence[Message] = ()) -> AsyncGenerator[str, None]:
        if self.provider == "local":
            history_text = "\n".join(f"{role.title()}: {content}" for role, content in history)
            if history_text:
                prompt = f"Conversation history:\n{history_text}\n\nCurrent request:\n{prompt}"
            async for chunk in self._ollama.generate_stream(prompt=prompt, system=system):
                yield chunk
            return

        request_format = self._request_format()
        if request_format == "openai":
            payload: dict[str, Any] = {
                "model": self._resolved_model(),
                "messages": self._openai_messages(prompt, system, history),
                "max_completion_tokens": 2048,
                "temperature": 0.2,
                "top_p": 0.95,
                "stream": True,
            }
            async with self._client.stream("POST", f"{self._resolved_base_url()}/chat/completions", headers=self._request_headers(), json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    data_str = line.removeprefix("data: ")
                    if data_str == "[DONE]":
                        break
                    try:
                        choices = json.loads(data_str).get("choices") or []
                        if choices:
                            text = (choices[0].get("delta") or {}).get("content", "")
                            if text:
                                yield text
                    except json.JSONDecodeError:
                        continue
            return

        if request_format == "anthropic":
            payload = {
                "model": self._resolved_model(),
                "max_tokens": 2048,
                "temperature": 1.0,
                "top_p": 0.95,
                "stream": True,
                "messages": self._anthropic_messages(prompt, history),
            }
            if system:
                payload["system"] = system
            async with self._client.stream("POST", f"{self._resolved_base_url()}/v1/messages", headers=self._request_headers(), json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue
                    try:
                        data = json.loads(line.removeprefix("data: "))
                        if data.get("type") == "content_block_delta":
                            text = (data.get("delta") or {}).get("text", "")
                            if text:
                                yield text
                        elif data.get("type") == "message_stop":
                            break
                    except json.JSONDecodeError:
                        continue
            return

        raise ValueError(f"Unsupported provider for streaming: {self.provider}")

    async def close(self):
        await self._client.aclose()
        await self._ollama.close()
