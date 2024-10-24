from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
import ollama

app = FastAPI()


class Answer(BaseModel):
    question: str
    answer: str


@app.post("/question")
async def question(request: Request):
    question = (await request.body()).decode()
    client = ollama.AsyncClient()
    messages = [{'role': 'user', 'content': question}]
    response = await client.chat(model="llama3.2", messages=messages)
    answer = response['message']['content']
    return Answer(question=question, answer=answer)
