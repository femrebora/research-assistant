"""Text embedding via LiteLLM (uses any configured provider)."""

from __future__ import annotations

import os
import time

from dotenv import load_dotenv

load_dotenv()

DEFAULT_EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")


def embed_texts(
    texts: list[str],
    model: str = DEFAULT_EMBED_MODEL,
    max_retries: int = 3,
) -> list[list[float]]:
    """Embed a batch of texts. Retries on failure with exponential backoff."""
    import litellm as _litellm

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = _litellm.embedding(model=model, input=texts)
            return [d["embedding"] for d in response.data]  # type: ignore[index]
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(2 ** attempt)

    raise RuntimeError(
        f"All {max_retries} embedding retries failed. Last error: {last_error}"
    )


def embed_single(text: str, model: str = DEFAULT_EMBED_MODEL) -> list[float]:
    """Embed a single text string."""
    return embed_texts([text], model=model)[0]
