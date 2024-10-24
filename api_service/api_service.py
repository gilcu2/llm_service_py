from fastapi import FastAPI, Request, Body
from common.model import QuestionAnswer

app = FastAPI()


@app.post("/question")
async def question(request: Request):
    question = (await request.body()).decode()

    return QuestionAnswer(question=question, answer="Hi")

@app.get("/hello")
async def question(request: Request):
    return QuestionAnswer(question="Hello", answer="Hi")