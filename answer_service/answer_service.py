from fastapi import FastAPI, Request, BackgroundTasks
import ollama
from common.model import QuestionAnswer
from common.kafka import send_to_kafka
import random

app = FastAPI()


@app.post("/question_ollama")
async def question(request: Request, background_tasks: BackgroundTasks):
    question = (await request.body()).decode()
    client = ollama.AsyncClient()
    messages = [{'role': 'user', 'content': question}]
    response = await client.chat(model="llama3.2", messages=messages)
    answer = response['message']['content']
    qa = QuestionAnswer(question=question, answer=answer)
    background_tasks.add_task(send_to_kafka, qa=qa)
    return qa

@app.post("/question")
async def question(request: Request, background_tasks: BackgroundTasks):
    question = (await request.body()).decode()
    qa = QuestionAnswer(question=question, answer=f"The answer is {random.randint(1, 1000)}")
    send_to_kafka(qa)
    return qa

@app.get("/hello")
async def question(request: Request):
    return QuestionAnswer(question="Hello", answer="Hi")