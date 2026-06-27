import os
import httpx
from typing import AsyncGenerator


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")
        self._client = httpx.AsyncClient(timeout=120.0)

    async def generate(self, prompt: str, system: str = "") -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        response = await self._client.post(
            f"{self.base_url}/api/generate",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    async def generate_stream(self, prompt: str, system: str = "") -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
        }
        if system:
            payload["system"] = system

        async with self._client.stream(
            "POST",
            f"{self.base_url}/api/generate",
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    try:
                        data = __import__('json').loads(line)
                        chunk = data.get("response", "")
                        if chunk:
                            yield chunk
                    except:
                        continue

    async def close(self):
        await self._client.aclose()
