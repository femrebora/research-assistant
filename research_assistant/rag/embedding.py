"""Text embedding via LiteLLM (uses any configured provider)."""

from __future__ import annotations

import logging
import os
import time

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")

# Error-substring markers that indicate a permanent config/auth problem.
# Retrying these is wasteful — fail fast so the user sees the real cause.
_CONFIG_ERROR_MARKERS: tuple[str, ...] = (
    "auth",
    "api_key",
    "api key",
    "key",
    "permission",
    "unauthorized",
    "forbidden",
    "invalid",
    "model",
    "not found",
    "does not exist",
    "no such",
    "deployment",
    "disabled",
)


def _is_config_error(exc: Exception) -> bool:
    """Return True when the exception looks like a permanent config/auth failure."""
    msg = str(exc).lower()
    return any(marker in msg for marker in _CONFIG_ERROR_MARKERS)


def embed_texts(
    texts: list[str],
    model: str = DEFAULT_EMBED_MODEL,
    max_retries: int = 3,
) -> list[list[float]]:
    """Embed a batch of texts.

    Retries transient failures (rate-limit, timeout, network) with exponential
    backoff.  Config/auth errors fail immediately — retrying them only wastes
    time and buries the real cause.
    """
    import litellm as _litellm

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = _litellm.embedding(model=model, input=texts)
            return [d["embedding"] for d in response.data]  # type: ignore[index]
        except Exception as e:
            last_error = e
            if _is_config_error(e):
                logger.error("Embedding config/auth error (not retrying): %s", e)
                raise
            if attempt < max_retries:
                wait = 2 ** attempt
                logger.warning(
                    "Embedding attempt %d/%d failed (transient), retrying in %ds: %s",
                    attempt, max_retries, wait, e,
                )
                time.sleep(wait)

    raise RuntimeError(
        f"All {max_retries} embedding retries failed. Last error: {last_error}"
    )


def embed_single(text: str, model: str = DEFAULT_EMBED_MODEL) -> list[float]:
    """Embed a single text string."""
    return embed_texts([text], model=model)[0]
