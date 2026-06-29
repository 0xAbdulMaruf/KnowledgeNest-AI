import os
from typing import Any, AsyncGenerator

import httpx

from app.llm.ollama_client import OllamaClient


class AIProviderClient:
    def __init__(self, provider: str = "local", base_url: str | None = None, api_key: str | None = None, model: str | None = None):
        self.provider = provider
        self.base_url = (base_url or "").strip()
        self.api_key = (api_key or "").strip()
        self.model = (model or "").strip()
        self._client = httpx.AsyncClient(timeout=120.0)
        self._ollama = OllamaClient(base_url=self.base_url or None, model=self.model or None)

    def _resolved_base_url(self) -> str:
        if self.base_url:
            return self.base_url.rstrip("/")
        if self.provider == "anthropic":
            return "https://api.anthropic.com/v1"
        if self.provider == "mimo":
            return "https://api.xiaomimimo.com/v1"
        if self.provider == "openai":
            return "https://api.openai.com/v1"
        return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")

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
            base_url = self._resolved_base_url()
            if base_url.rstrip("/").endswith("/anthropic"):
                return "anthropic"
            return "openai"
        if self.provider == "openai":
            return "openai"
        return "local"

    def _request_headers(self) -> dict[str, str]:
        if self.provider in {"openai", "mimo", "anthropic"}:
            headers = {"api-key": self.api_key, "Content-Type": "application/json"}
            if self.provider == "anthropic":
                headers["anthropic-version"] = "2023-06-01"
            return headers
        return {"Content-Type": "application/json"}

    async def test_connection(self) -> None:
        await self.generate(prompt="Reply with OK.", system="You are a test assistant.")

    async def generate(self, prompt: str, system: str = "") -> str:
        if self.provider == "local":
            return await self._ollama.generate(prompt=prompt, system=system)

        request_format = self._request_format()

        if request_format == "openai":
            payload: dict[str, Any] = {
                "model": self._resolved_model(),
                "messages": [],
                "max_completion_tokens": 1024,
                "temperature": 0.2,
                "top_p": 0.95,
                "stream": False,
            }
            if system:
                payload["messages"].append({"role": "system", "content": system})
            payload["messages"].append({"role": "user", "content": prompt})

            response = await self._client.post(
                f"{self._resolved_base_url()}/chat/completions",
                headers=self._request_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices") or []
            if not choices:
                return ""
            message = choices[0].get("message") or {}
            return str(message.get("content", ""))

        if request_format == "anthropic":
            payload = {
                "model": self._resolved_model(),
                "max_tokens": 1024,
                "temperature": 1.0,
                "top_p": 0.95,
                "stream": False,
                "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            }
            if system:
                payload["system"] = system

            response = await self._client.post(
                f"{self._resolved_base_url()}/v1/messages",
                headers=self._request_headers(),
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            content = data.get("content") or []
            parts = [str(item.get("text", "")) for item in content if isinstance(item, dict)]
            return "".join(parts)

        raise ValueError(f"Unsupported provider: {self.provider}")

    async def generate_stream(self, prompt: str, system: str = "") -> AsyncGenerator[str, None]:
        answer = await self.generate(prompt=prompt, system=system)
        if answer:
            yield answer

    async def close(self):
        await self._client.aclose()
        await self._ollama.close()