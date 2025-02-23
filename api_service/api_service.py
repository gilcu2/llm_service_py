from fastapi import FastAPI, Request, Body
from common.model import QuestionAnswer
import httpx
import os

app = FastAPI()

ANSWER_ENDPOINT=os.getenv("ANSWER_ENDPOINT","localhost:8082")

@app.post("/question")
async def question(request: Request):
    question = (await request.body())
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{ANSWER_ENDPOINT}/question', content=question)
    qa = QuestionAnswer.model_validate_json(r.text)
    return qa

