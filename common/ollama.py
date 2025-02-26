import logging
import os
import sys

import ollama

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "localhost:11434")
logger.debug(f"Ollamaendpoint: {OLLAMA_ENDPOINT}")


async def ask_ollama(question: str) -> str:
    client = ollama.AsyncClient(host=f"http://{OLLAMA_ENDPOINT}")
    messages = [{"role": "user", "content": question}]
    response = await client.chat(model="llama3.2", messages=messages)
    return response["message"]["content"]
