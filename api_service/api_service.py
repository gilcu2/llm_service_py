from fastapi import FastAPI
from common.model import Question, QuestionAnswer
import httpx
import os

app = FastAPI()

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "localhost:8082")
HISTORY_ENDPOINT = os.getenv("HISTORY_ENDPOINT", "localhost:8083")


async def ask_question(question: Question) -> QuestionAnswer:
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{LLM_ENDPOINT}/query', json=dict(question))
    qa = QuestionAnswer.model_validate_json(r.text)
    return qa


async def save_question_answer(qa: QuestionAnswer) -> bool:
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{HISTORY_ENDPOINT}/save', json=dict(qa))
    return r.is_success


@app.post("/question")
async def question(question: Question):
    qa = await ask_question(question)
    await save_question_answer(qa)
    return qa


@app.get("/history")
async def question(question: Question):
    qa = await ask_question(question)
    await save_question_answer(qa)
    return qa