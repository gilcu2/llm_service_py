from fastapi import FastAPI, Request
from common.postgres import get_latest
from common.model import QuestionAnswer

app = FastAPI()


@app.get("/history/")
async def question(limit: int = 10):
    qas = get_latest(limit)
    return qas


@app.get("/hello")
async def question(request: Request):
    return QuestionAnswer(question="Hello", answer="Hi")
