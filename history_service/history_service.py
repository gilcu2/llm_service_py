from fastapi import BackgroundTasks, FastAPI

from common.model import QuestionAnswer
from common.postgres import create_table, get_latest, insert_data

app = FastAPI()


@app.get("/history/")
async def get_latest_histories(limit: int = 10):
    qas = await get_latest(limit)
    return qas


@app.post("/history")
async def add_history(qa: QuestionAnswer, background_tasks: BackgroundTasks):
    background_tasks.add_task(insert_data, qa)


if __name__ == "__main__":
    create_table()
