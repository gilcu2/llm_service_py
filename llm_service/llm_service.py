from fastapi import FastAPI, Request
import ollama
from common.model import Question, QuestionAnswer

import random
import os
import sys
import logging

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "localhost:11434")
logger.debug(f"Ollamaendpoint: {OLLAMA_ENDPOINT}")


async def ask_ollama(question: str) -> str:
    client = ollama.AsyncClient(host=f"http://{OLLAMA_ENDPOINT}")
    messages = [{'role': 'user', 'content': question.question}]
    response = await client.chat(model="llama3.2:1b", messages=messages)
    return response['message']['content']


@app.post("/question")
async def question(question: Question):
    answer = await ask_ollama(question.question)
    qa = QuestionAnswer(question=question.question, answer=answer)
    return qa
