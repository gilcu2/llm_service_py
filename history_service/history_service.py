from fastapi import FastAPI, Request, BackgroundTasks
from common.postgres import get_latest
from common.model import QuestionAnswer
from common.postgres import insert_data, create_table

create_table()
app = FastAPI()


@app.get("/history/")
async def get_latest_histories(limit: int = 10):
    qas = await get_latest(limit)
    return qas


@app.post("/history")
async def add_history(qa: QuestionAnswer, background_tasks: BackgroundTasks):
    background_tasks.add_task(insert_data, qa)
