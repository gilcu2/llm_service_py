from fastapi import FastAPI, Request, BackgroundTasks
import ollama
from common.model import QuestionAnswer
from common.postgres import insert_data
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


@app.post("/question_ollama")
async def question(request: Request, background_tasks: BackgroundTasks):
    question = (await request.body()).decode()
    client = ollama.AsyncClient(host=f"http://{OLLAMA_ENDPOINT}")
    messages = [{'role': 'user', 'content': question}]
    response = await client.chat(model="llama3.2", messages=messages)
    answer = response['message']['content']
    qa = QuestionAnswer(question=question, answer=answer)
    background_tasks.add_task(insert_data, qa)
    return qa


@app.post("/question_random")
async def question(request: Request, background_tasks: BackgroundTasks):
    question = (await request.body()).decode()
    qa = QuestionAnswer(question=question, answer=f"The answer is {random.randint(1, 1000)}")
    background_tasks.add_task(insert_data, qa)
    return qa


@app.get("/hello")
async def question(request: Request):
    return QuestionAnswer(question="Hello", answer="Hi")
