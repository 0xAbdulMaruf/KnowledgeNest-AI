import json
import os
from typing import AsyncGenerator

import httpx


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=15.0))

    async def generate(self, prompt: str, system: str = "") -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": {"num_predict": 2048}}
        if system:
            payload["system"] = system
        response = await self._client.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()
        return str(response.json().get("response", ""))

    async def generate_stream(self, prompt: str, system: str = "") -> AsyncGenerator[str, None]:
        payload = {"model": self.model, "prompt": prompt, "stream": True, "options": {"num_predict": 2048}}
        if system:
            payload["system"] = system
        async with self._client.stream("POST", f"{self.base_url}/api/generate", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line).get("response", "")
                    if chunk:
                        yield chunk
                except json.JSONDecodeError:
                    continue

    async def close(self):
        await self._client.aclose()
