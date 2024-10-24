from pyexpat.errors import messages

from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
import ollama

app = FastAPI()


class Answer(BaseModel):
    question: str
    answer: str

@app.post("/question")
async def question(request: Request):
    question=(await request.body()).decode()
    return Answer(question=question, answer="Hi")