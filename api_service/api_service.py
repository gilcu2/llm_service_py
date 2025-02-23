from fastapi import FastAPI, Request,  BackgroundTasks
from common.model import QuestionAnswer
import httpx
import os
from common.postgres import insert_data

app = FastAPI()

ANSWER_ENDPOINT = os.getenv("ANSWER_ENDPOINT", "localhost:8082")


async def post_question(question: str) -> QuestionAnswer:
    async with httpx.AsyncClient() as client:
        r = await client.post(f'http://{ANSWER_ENDPOINT}/question', content=question)
    qa = QuestionAnswer.model_validate_json(r.text)
    return qa


@app.post("/question")
async def question(request: Request, background_tasks: BackgroundTasks):
    question = (await request.body())
    qa = await post_question(question)
    background_tasks.add_task(insert_data, qa)
    return qa
