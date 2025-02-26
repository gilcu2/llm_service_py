from fastapi import FastAPI
from common.model import Question, QuestionAnswer
import httpx
import os
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

app = FastAPI()

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "localhost:8082")
HISTORY_ENDPOINT = os.getenv("HISTORY_ENDPOINT", "localhost:8083")

logger.info(f"LLM_ENDPOINT: {LLM_ENDPOINT}")
logger.info(f"HISTORY_ENDPOINT: {HISTORY_ENDPOINT}")


async def ask_question(question: Question) -> QuestionAnswer:
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{LLM_ENDPOINT}/question', json=dict(question))
    qa = QuestionAnswer.model_validate_json(r.text)
    return qa


async def to_history(qa: QuestionAnswer) -> bool:
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{HISTORY_ENDPOINT}/history', json=dict(qa))
    return r.is_success


async def get_histories(limit: int = 10) -> list[QuestionAnswer]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://{HISTORY_ENDPOINT}/history/?limit={limit}')
    r = []
    for d in response.json():
        r.append(QuestionAnswer.model_validate(d))
    return r


@app.post("/question")
async def question(question: Question):
    qa = await ask_question(question)
    await to_history(qa)
    return qa


@app.get("/history/")
async def history(limit: int = 10):
    qa = await get_histories(limit)
    return qa
