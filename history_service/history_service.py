from fastapi import FastAPI, Request
from common.kafka import get_from_kafka
from common.model import QuestionAnswer

app = FastAPI()


@app.get("/history/")
async def question(limit: int = 10):
    msgs = get_from_kafka(limit)
    return msgs


@app.get("/hello")
async def question(request: Request):
    return QuestionAnswer(question="Hello", answer="Hi")
