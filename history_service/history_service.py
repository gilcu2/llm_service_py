from fastapi import FastAPI, Request,  BackgroundTasks
from common.postgres import get_latest
from common.model import QuestionAnswer
from common.postgres import insert_data

app = FastAPI()


@app.get("/history/")
async def question(limit: int = 10):
    qas = get_latest(limit)
    return qas


@app.post("/history")
async def question(qa:, background_tasks: BackgroundTasks):

    background_tasks.add_task(insert_data, qa)

